#!/usr/bin/env python3
"""Render the final CI job, retaining a repository's existing mandatory jobs.

This module does not contact GitHub or modify workflows. The rollout records
the inspected dependency list per repository. Do not infer it from job names.
"""

import json
import textwrap


GATE = '''import json, os, sys
needs = json.loads(os.environ["NEEDS_JSON"])
expected = json.loads(os.environ["EXPECTED_JOBS"])
if not expected or set(needs) != set(expected):
    sys.exit("Missing or unexpected required jobs")
failed = {name: job.get("result") for name, job in needs.items()
          if job.get("result") != "success"}
if failed:
    sys.exit("Required jobs did not succeed: " + json.dumps(failed))
for job, output, field in json.loads(os.environ["MATRIX_OUTPUTS"]):
    matrix = json.loads(needs[job]["outputs"][output])
    entries = matrix[field] if field else matrix
    if not isinstance(entries, list) or not entries:
        sys.exit("Empty or invalid required matrix: " + job)
print("All required jobs succeeded")
'''


def render_job(jobs, matrices=()):
    if not jobs or len(set(jobs)) != len(jobs):
        raise ValueError("Expected a nonempty list of unique required job IDs")
    if any(job not in jobs for job, _, _ in matrices):
        raise ValueError("Matrix producer must be a required job")
    header = (
        "\n  # Stable branch-protection check; every required matrix job must pass.\n"
        "  ci:\n"
        "    name: ci\n"
        "    if: ${{ always() }}\n"
        "    needs: " + json.dumps(jobs) + "\n"
        "    runs-on: ubuntu-latest\n"
        "    timeout-minutes: 5\n"
        "    permissions: {}\n"
        "    steps:\n"
        "      - name: Require all mandatory jobs to succeed\n"
        "        env:\n"
        "          NEEDS_JSON: ${{ toJSON(needs) }}\n"
        "          EXPECTED_JOBS: '" + json.dumps(jobs) + "'\n"
        "          MATRIX_OUTPUTS: '" + json.dumps(matrices) + "'\n"
        "        shell: python\n"
        "        run: |\n"
    )
    return header + textwrap.indent(GATE, "          ")
