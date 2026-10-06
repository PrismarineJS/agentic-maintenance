import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from required_ci import GATE, render_job


class RequiredCiTests(unittest.TestCase):
    def run_gate(self, needs, expected=("tests",), matrices=()):
        env = dict(os.environ, NEEDS_JSON=json.dumps(needs),
                   EXPECTED_JOBS=json.dumps(expected),
                   MATRIX_OUTPUTS=json.dumps(matrices))
        return subprocess.run([sys.executable, "-c", GATE], env=env,
                              capture_output=True, text=True)

    def test_success(self):
        self.assertEqual(self.run_gate({"tests": {"result": "success"}}).returncode, 0)

    def test_failures_and_skips_are_not_success(self):
        for result in ("failure", "cancelled", "skipped", "neutral", None):
            with self.subTest(result=result):
                self.assertNotEqual(self.run_gate({"tests": {"result": result}}).returncode, 0)

    def test_missing_extra_and_empty_dependencies_fail(self):
        for needs, expected in (({}, ["tests"]), ({}, []),
                                ({"tests": {"result": "success"}, "extra": {}}, ["tests"])):
            self.assertNotEqual(self.run_gate(needs, expected).returncode, 0)

    def test_dynamic_matrix_must_exist_and_be_nonempty(self):
        for matrix, ok in (({"include": [{"version": "1.21"}]}, True),
                           ({"include": []}, False), ({}, False),
                           ({"include": "not an array"}, False)):
            needs = {"prepare": {"result": "success", "outputs": {"matrix": json.dumps(matrix)}},
                     "tests": {"result": "success"}}
            result = self.run_gate(needs, ["prepare", "tests"], [("prepare", "matrix", "include")])
            self.assertEqual(result.returncode == 0, ok)

    def test_gate_always_runs_after_dependencies(self):
        rendered = render_job(["lint", "tests"])
        self.assertIn("if: ${{ always() }}", rendered)
        self.assertIn('needs: ["lint", "tests"]', rendered)
        self.assertIn("permissions: {}", rendered)
        with self.assertRaises(ValueError):
            render_job([])
        with self.assertRaises(ValueError):
            render_job(["tests"], [("missing", "matrix", "include")])
