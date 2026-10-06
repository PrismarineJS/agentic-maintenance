#!/usr/bin/env python3
"""Read-only policy diff. Python 3 stdlib + authenticated gh; no apply mode.

Live: python3 scripts/audit_branch_policy.py --live --output /tmp/pjs-policy
Replay: python3 scripts/audit_branch_policy.py --snapshot /tmp/audit.json --output /tmp/pjs-policy
Writes PREFIX.json (replayable evidence and proposed changes) and PREFIX.md.
"""

import argparse
import concurrent.futures
import datetime
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_KEYS = ("name", "target", "enforcement", "bypass_actors", "conditions", "rules")


def get(endpoint, paginate=False):
    # Fixed GET: neither CLI input nor the policy can select a mutation method.
    command = ["gh", "api", "--method", "GET", endpoint]
    if paginate:
        command.append("--paginate")
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"ok": False, "data": None, "error": str(error)}
    raw = result.stdout.strip()
    try:
        if paginate and result.returncode == 0:
            data = []
            decoder = json.JSONDecoder()
            while raw:
                page, end = decoder.raw_decode(raw)
                if not isinstance(page, list):
                    raise ValueError("Expected an array page")
                data.extend(page)
                raw = raw[end:].strip()
        else:
            data = json.loads(raw)
    except (ValueError, TypeError):
        return {"ok": False, "data": None, "error": "Invalid or missing API JSON"}
    return {"ok": result.returncode == 0, "data": data,
            "error": result.stderr.strip() if result.returncode else None}


def capture(repository):
    name = repository["name"]
    record = {"name": name, "default_branch": repository["default_branch"],
              "archived": repository["archived"], "private": repository["private"],
              "url": repository["html_url"],
              "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    if record["private"]:
        # The report may be checked into a public repository. Do not disclose
        # names, branch names, workflows, or URLs of excluded private repos.
        record.update(name="[private repository]", default_branch=None, url=None)
        return record
    if record["archived"]:
        return record
    repo = repository["full_name"]
    branch = quote(record["default_branch"], safe="")
    endpoints = {
        "protection": f"repos/{repo}/branches/{branch}/protection",
        "rulesets": f"repos/{repo}/rulesets?includes_parents=true&per_page=100",
        "effective_rules": f"repos/{repo}/rules/branches/{branch}?per_page=100",
        "workflows": f"repos/{repo}/actions/workflows?per_page=100",
    }
    for key, endpoint in endpoints.items():
        record[key] = get(endpoint, paginate=key in ("rulesets", "effective_rules"))
    record["ruleset_details"] = {}
    if record["rulesets"]["ok"]:
        for rule in record["rulesets"]["data"]:
            if rule.get("source_type") == "Repository" and rule.get("source") == repo:
                record["ruleset_details"][str(rule["id"])] = get(
                    f"repos/{repo}/rulesets/{rule['id']}")
    return record


def canonical(value):
    """Ordering of rules/checks/actors does not change these policy payloads."""
    if isinstance(value, dict):
        return {k: canonical(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        return sorted((canonical(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    return value


def ruleset_diff(current, desired):
    actual = {k: current.get(k) for k in PAYLOAD_KEYS}
    return {k: {"current": actual[k], "proposed": desired[k]}
            for k in PAYLOAD_KEYS if canonical(actual[k]) != canonical(desired[k])}


def analyze(record, policy):
    if record["private"] or record["archived"]:
        return {"name": "[private repository]" if record["private"] else record["name"],
                "excluded": "private" if record["private"] else "archived"}
    p = record["protection"]
    absent = not p["ok"] and isinstance(p["data"], dict) and p["data"].get("message") == "Branch not protected"
    protection = "present" if p["ok"] else "absent" if absent else "unknown"
    data = p["data"] if p["ok"] else {}
    checks = data.get("required_status_checks") or {}
    reviews = data.get("required_pull_request_reviews") or {}
    errors = [k for k in ("rulesets", "effective_rules", "workflows") if not record[k]["ok"]]
    if protection == "unknown":
        errors.append("protection")
    plan = []
    for desired in policy["rulesets"]:
        entry = {"name": desired["name"], "action": "unknown"}
        if record["rulesets"]["ok"]:
            matching = [r for r in record["rulesets"]["data"] if r["name"] == desired["name"]]
            if not matching:
                entry["action"] = "create_after_prerequisites"
            elif len(matching) != 1 or matching[0].get("source_type") != "Repository" or matching[0].get("source") != policy["organization"] + "/" + record["name"]:
                entry["action"] = "manual_reconciliation"
            else:
                detail = record.get("ruleset_details", {}).get(str(matching[0]["id"]), {})
                if detail.get("ok"):
                    entry["id"] = matching[0]["id"]
                    entry["diff"] = ruleset_diff(detail["data"], desired)
                    entry["action"] = "review_update" if entry["diff"] else "matches"
                else:
                    errors.append("ruleset_details")
        plan.append(entry)
    managed = {r["name"] for r in policy["rulesets"]}
    others = [r["name"] for r in record["rulesets"]["data"] if r["name"] not in managed] if record["rulesets"]["ok"] else []
    workflows = record["workflows"]["data"].get("workflows", []) if record["workflows"]["ok"] else []
    if record["workflows"]["ok"] and record["workflows"]["data"].get("total_count", 0) > len(workflows):
        errors.append("workflow_inventory_truncated")
    return {
        "name": record["name"], "default_branch": record["default_branch"], "url": record["url"],
        "current": {"classic_protection": protection,
                    "pr_required": bool(reviews) if protection != "unknown" else None,
                    "approvals": reviews.get("required_approving_review_count", 0) if protection != "unknown" else None,
                    "checks": checks.get("contexts", []) if protection != "unknown" else None,
                    "strict": checks.get("strict", False) if protection != "unknown" else None,
                    "admin_enforcement": data.get("enforce_admins", {}).get("enabled", False) if protection != "unknown" else None,
                    "force_push_allowed": data.get("allow_force_pushes", {}).get("enabled", True) if protection != "unknown" else None,
                    "effective_ruleset_rule_count": len(record["effective_rules"]["data"]) if record["effective_rules"]["ok"] else None},
        "proposed_rulesets": plan,
        "classic_reconciliation": protection == "present",
        "other_rulesets_to_preserve": others,
        "read_errors": sorted(set(errors)),
        "workflow_paths": [w["path"] for w in workflows if w["state"] == "active" and w["path"].startswith(".github/")],
        "activation_readiness": "not_assessed",
        "prerequisites": ["Verify real ci gate, its source, complete matrix and negative controls",
                          "Inspect automation for direct default-branch pushes",
                          "Refresh and reconcile all applicable rules without weakening other branches"],
    }


def make_report(records, policy):
    supported_scope = {"visibility": "public", "include_archived": False,
                       "include_forks": True, "branch": "~DEFAULT_BRANCH"}
    if policy["scope"] != supported_scope:
        raise ValueError("This auditor supports public, unarchived repositories (including forks), default branch only")
    # Sanitize replayed historical snapshots as well as live collection.
    evidence = [{"name": "[private repository]", "private": True, "archived": x["archived"],
                 "retrieved_at": x.get("retrieved_at")} if x["private"] else x for x in records]
    rows = [analyze(x, policy) for x in sorted(evidence, key=lambda x: x["name"].lower())]
    included = [r for r in rows if "excluded" not in r]
    summary = {
        "inventoried": len(rows), "included": len(included),
        "archived_excluded": sum(r.get("excluded") == "archived" for r in rows),
        "private_excluded": sum(r.get("excluded") == "private" for r in rows),
        "classic_to_reconcile": sum(r["classic_reconciliation"] for r in included),
        "no_classic_protection": sum(r["current"]["classic_protection"] == "absent" for r in included),
        "required_pr": sum(r["current"]["pr_required"] is True for r in included),
        "named_checks": sum(bool(r["current"]["checks"]) for r in included),
        "ci_admin_bypass_to_remove": sum(r["current"]["admin_enforcement"] is False and r["current"]["classic_protection"] == "present" for r in included),
        "rulesets_to_create_after_prerequisites": sum(p["action"] == "create_after_prerequisites" for r in included for p in r["proposed_rulesets"]),
        "repositories_with_read_errors": sum(bool(r["read_errors"]) for r in included),
        "activation_readiness_assessed": 0,
    }
    return {"generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "mode": "read_only_proposal", "policy": policy, "summary": summary,
            "repositories": rows, "evidence": evidence}


def markdown(report):
    s = report["summary"]
    lines = ["# Proposed default-branch settings diff", "",
             "Date: " + report["generated_at"] + ". Source: GitHub GET-only audit.", "",
             "No settings changed. The JSON companion contains the exact desired rulesets, current evidence, and per-repository diff.", "",
             "## Scope", "", f"- {s['inventoried']} repositories inventoried; {s['included']} public, unarchived repositories included.",
             f"- {s['archived_excluded']} archived and {s['private_excluded']} private repositories excluded.",
             f"- {s['rulesets_to_create_after_prerequisites']} proposed ruleset creations after CI/automation prerequisites; {s['classic_to_reconcile']} classic protections to reconcile.",
             f"- {s['no_classic_protection']} default branches have no classic protection; {s['required_pr']} require a PR; {s['named_checks']} name required checks.",
             f"- {s['repositories_with_read_errors']} included repositories have read errors. Activation readiness is not certified for any repository by this settings audit.", "",
             "## Intended behavior", "", "All included repositories: `ci` from GitHub Actions, up-to-date branch, no force pushes/deletion, no CI bypass. PR plus one approval, with repository-admin bypass **for PRs only**. Two independent rulesets keep that exception out of CI.", "",
             "Admins can merge a passing unapproved PR. They cannot use this exception to merge failing CI or push directly. Private repositories remain outside enforceable coverage on this plan.", "",
             "## Per-repository proposal", "",
             "These current PR/check columns describe classic protection; consult the JSON evidence for any additional rulesets. A ruleset creation/update is deferred until repository-specific CI and automation have been validated. Existing classic patterns must be inspected before retiring them.", "",
             "| Repository | Default branch | Current PR / approvals | Current required checks | Proposed rulesets | Classic protection |",
             "|---|---|---|---|---|---|"]
    for r in report["repositories"]:
        if "excluded" in r:
            continue
        c = r["current"]
        pr = "Unknown" if c["pr_required"] is None else f"Yes / {c['approvals']}" if c["pr_required"] else "No"
        checks = "Unknown" if c["checks"] is None else ", ".join(c["checks"]) or "None"
        actions = "; ".join(p["name"] + ": " + p["action"] for p in r["proposed_rulesets"])
        classic = "Reconcile after replacement" if r["classic_reconciliation"] else c["classic_protection"]
        lines.append(f"| [{r['name']}]({r['url']}/settings/rules) | `{r['default_branch']}` | {pr} | {checks} | {actions} | {classic} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--live", action="store_true")
    mode.add_argument("--snapshot", type=Path)
    parser.add_argument("--policy", type=Path, default=ROOT / "policies/default_branch.json")
    parser.add_argument("--output", type=Path, required=True, help="Output prefix for local .json and .md files")
    args = parser.parse_args()
    policy = json.loads(args.policy.read_text())
    if args.live:
        inventory = get(f"orgs/{policy['organization']}/repos?per_page=100&type=all", paginate=True)
        if not inventory["ok"]:
            parser.error("Could not read complete organization inventory: " + str(inventory["error"]))
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            records = list(executor.map(capture, inventory["data"]))
    else:
        saved = json.loads(args.snapshot.read_text())
        records = saved["evidence"] if isinstance(saved, dict) else saved
    report = make_report(records, policy)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    Path(str(args.output) + ".json").write_text(json.dumps(report, indent=2) + "\n")
    Path(str(args.output) + ".md").write_text(markdown(report))
    print(json.dumps(report["summary"], indent=2))
    return 1 if report["summary"]["repositories_with_read_errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
