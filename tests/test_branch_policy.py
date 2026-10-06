"""Offline checks for the policy's permission boundaries and audit failures."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("audit", ROOT / "scripts/audit_branch_policy.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)
POLICY = json.loads((ROOT / "policies/default_branch.json").read_text())


def reply(data, ok=True):
    return {"ok": ok, "data": data, "error": None if ok else "request failed"}


def repository():
    return {"name": "example", "url": "https://github.com/PrismarineJS/example",
            "default_branch": "src", "private": False, "archived": False,
            "protection": reply({"message": "Branch not protected", "status": "404"}, False),
            "rulesets": reply([]), "effective_rules": reply([]),
            "workflows": reply({"total_count": 0, "workflows": []}), "ruleset_details": {}}


class PolicyTests(unittest.TestCase):
    def test_admin_exception_cannot_bypass_ci_or_allow_direct_push(self):
        ci, review = POLICY["rulesets"]
        self.assertEqual(ci["bypass_actors"], [])
        self.assertEqual(review["bypass_actors"], [
            {"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "pull_request"}])
        self.assertEqual([r["type"] for r in review["rules"]], ["pull_request"])
        self.assertEqual(review["rules"][0]["parameters"]["required_approving_review_count"], 1)
        rules = {r["type"]: r for r in ci["rules"]}
        self.assertTrue({"deletion", "non_fast_forward"}.issubset(rules))
        checks = rules["required_status_checks"]["parameters"]
        self.assertEqual(checks["required_status_checks"], [{"context": "ci", "integration_id": 15368}])
        self.assertTrue(checks["strict_required_status_checks_policy"])
        for rule in POLICY["rulesets"]:
            self.assertEqual(rule["conditions"]["ref_name"], {"include": ["~DEFAULT_BRANCH"], "exclude": []})

    def test_missing_protection_diff_is_deferred_not_ready(self):
        row = audit.analyze(repository(), POLICY)
        self.assertEqual(row["default_branch"], "src")
        self.assertFalse(row["current"]["pr_required"])
        self.assertEqual(row["activation_readiness"], "not_assessed")
        self.assertEqual([r["action"] for r in row["proposed_rulesets"]], ["create_after_prerequisites"] * 2)

    def test_permission_failure_is_not_an_unprotected_branch(self):
        r = repository()
        r["protection"] = reply({"message": "Resource not accessible", "status": "403"}, False)
        r["rulesets"] = reply(None, False)
        row = audit.analyze(r, POLICY)
        self.assertEqual(row["current"]["classic_protection"], "unknown")
        self.assertIsNone(row["current"]["pr_required"])
        self.assertIsNone(row["current"]["checks"])
        self.assertIn("protection", row["read_errors"])
        self.assertTrue(all(x["action"] == "unknown" for x in row["proposed_rulesets"]))

    def test_private_evidence_is_redacted_and_archived_is_excluded(self):
        private = repository()
        private.update(private=True, name="confidential-name", default_branch="secret-branch")
        archived = repository()
        archived["archived"] = True
        report = audit.make_report([private, archived], POLICY)
        self.assertEqual(report["summary"]["included"], 0)
        self.assertEqual(report["summary"]["private_excluded"], 1)
        self.assertEqual(report["summary"]["archived_excluded"], 1)
        self.assertNotIn("confidential-name", json.dumps(report))
        self.assertNotIn("secret-branch", json.dumps(report))

    def test_existing_rules_detect_bypass_drift_not_ordering(self):
        desired = POLICY["rulesets"][0]
        actual = copy.deepcopy(desired)
        actual.update(id=123, created_at="yesterday")
        actual["rules"].reverse()
        self.assertEqual(audit.ruleset_diff(actual, desired), {})
        actual["bypass_actors"] = [{"actor_type": "RepositoryRole", "actor_id": 5, "bypass_mode": "always"}]
        self.assertEqual(set(audit.ruleset_diff(actual, desired)), {"bypass_actors"})

    def test_server_expanded_defaults_match_but_new_restrictions_do_not(self):
        desired = POLICY["rulesets"][1]
        actual = copy.deepcopy(desired)
        params = actual["rules"][0]["parameters"]
        params.update(copy.deepcopy(audit.PR_PARAMETER_DEFAULTS))
        self.assertEqual(audit.ruleset_diff(actual, desired), {})
        params["allowed_merge_methods"] = ["squash"]
        self.assertIn("rules", audit.ruleset_diff(actual, desired))
        params["allowed_merge_methods"] = ["merge", "squash", "rebase"]
        params["future_unknown_requirement"] = True
        self.assertIn("rules", audit.ruleset_diff(actual, desired))

    def test_inherited_name_collision_requires_manual_reconciliation(self):
        r = repository()
        r["rulesets"] = reply([{"id": 8, "name": POLICY["rulesets"][0]["name"],
                                "source_type": "Organization", "source": "PrismarineJS"}])
        row = audit.analyze(r, POLICY)
        self.assertEqual(row["proposed_rulesets"][0]["action"], "manual_reconciliation")

    def test_unreadable_rule_detail_is_not_a_match(self):
        r = repository()
        r["rulesets"] = reply([{"id": 8, "name": POLICY["rulesets"][0]["name"],
                                "source_type": "Repository", "source": "PrismarineJS/example"}])
        row = audit.analyze(r, POLICY)
        self.assertEqual(row["proposed_rulesets"][0]["action"], "unknown")
        self.assertIn("ruleset_details", row["read_errors"])

    def test_active_rulesets_count_even_without_classic_protection(self):
        r = repository()
        r["rulesets"] = reply([
            {"id": i, "name": rule["name"], "source_type": "Repository", "source": "PrismarineJS/example"}
            for i, rule in enumerate(POLICY["rulesets"])
        ])
        r["ruleset_details"] = {str(i): reply(copy.deepcopy(rule)) for i, rule in enumerate(POLICY["rulesets"])}
        summary = audit.make_report([r], POLICY)["summary"]
        self.assertEqual(summary["repositories_matching_policy"], 1)
        self.assertEqual(summary["review_rulesets_matching"], 1)
        self.assertEqual(summary["ci_rulesets_matching"], 1)
        r["ruleset_details"]["0"]["data"]["enforcement"] = "disabled"
        summary = audit.make_report([r], POLICY)["summary"]
        self.assertEqual(summary["repositories_matching_policy"], 0)
        self.assertEqual(summary["review_rulesets_matching"], 1)
        self.assertEqual(summary["ci_rulesets_matching"], 0)

    def test_get_only_transport_parses_every_page(self):
        result = subprocess.CompletedProcess([], 0, '[{"id":1}]\n[{"id":2}]', '')
        with patch.object(audit.subprocess, "run", return_value=result) as run:
            response = audit.get("orgs/PrismarineJS/repos?per_page=100", paginate=True)
        self.assertEqual(response["data"], [{"id": 1}, {"id": 2}])
        self.assertEqual(run.call_args.args[0][:4], ["gh", "api", "--method", "GET"])
        self.assertIn("--paginate", run.call_args.args[0])

    def test_timeout_is_an_explicit_read_error(self):
        with patch.object(audit.subprocess, "run", side_effect=subprocess.TimeoutExpired("gh", 120)):
            self.assertFalse(audit.get("orgs/PrismarineJS/repos")["ok"])


if __name__ == "__main__":
    unittest.main()
