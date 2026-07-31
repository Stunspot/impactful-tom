"""Executable fixtures for the dependency-free static verification scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run(script: str, *args: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPTS / script), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.returncode, json.loads(completed.stdout)


class StaticCheckFixtures(unittest.TestCase):
    def test_valid_fixture_passes_all_static_checks(self) -> None:
        repo = FIXTURES / "valid-repo"
        code, result = run("check_content_boundaries.py", "--repo", str(repo))
        self.assertEqual(code, 0, result)

        code, result = run("check_release_exclusions.py", "--repo", str(repo))
        self.assertEqual(code, 0, result)

        code, result = run(
            "check_distribution_topology.py",
            "--repo",
            str(repo),
            "--claude-root",
            str(FIXTURES / "valid-claude"),
            "--require-claude",
        )
        self.assertEqual(code, 0, result)

    def test_release_exclusions_reject_private_filename(self) -> None:
        code, result = run("check_release_exclusions.py", "--repo", str(FIXTURES / "leak-repo"))
        self.assertEqual(code, 1, result)
        self.assertTrue(any("release-excluded source filename" in item for item in result["errors"]))


if __name__ == "__main__":
    unittest.main()
