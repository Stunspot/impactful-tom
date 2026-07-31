"""Executable fixtures for the dependency-free static verification scripts."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
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


def copy_documentation_fixture(destination: Path) -> None:
    for relative in [
        "README.md",
        "CHANGELOG.md",
        "SUPPORT.md",
        "SECURITY.md",
        "DATA-AND-PRIVACY.md",
        "TERMS-OF-USE.md",
        "LICENSE.md",
        "ATTRIBUTION.md",
        "NOTICE.md",
        "TRADEMARKS.md",
        "documentation-manifest.json",
        "development/build_documentation_visuals.ps1",
        "development/documentation-project.json",
        "plugins/impactful-tom/assets/founder-constraint-mark.png",
        "verification/documentation/documentation-authorship.json",
        "verification/documentation/documentation-review.json",
        "verification/documentation/hesperos-pages-authoring-evidence.md",
        "verification/documentation/hesperos-pages-authoring-response.txt",
        "verification/documentation/visual-assets-custody.json",
    ]:
        source = REPO / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    shutil.copytree(REPO / "docs", destination / "docs")


class StaticCheckFixtures(unittest.TestCase):
    def test_public_documentation_site_passes_its_release_contract(self) -> None:
        code, result = run("check_documentation_site.py", "--repo", str(REPO))
        self.assertEqual(code, 0, result)

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

    def test_documentation_claim_gate_rejects_each_positive_host_overclaim(self) -> None:
        overclaims = [
            "Clean public-route installation is verified.",
            "Restart resilience has been observed.",
            "Causal host invocation is confirmed.",
            "Claude Code live behavior is healthy.",
            "Clean public-route installation works.",
            "Restart resilience passed.",
            "Causal host invocation is established.",
            "Claude Code live behavior is supported.",
        ]
        for overclaim in overclaims:
            with self.subTest(overclaim=overclaim), tempfile.TemporaryDirectory() as temp:
                candidate = Path(temp)
                copy_documentation_fixture(candidate)
                readme = candidate / "README.md"
                readme.write_text(
                    readme.read_text(encoding="utf-8") + f"\n\n{overclaim}\n",
                    encoding="utf-8",
                )
                code, result = run("check_documentation_site.py", "--repo", str(candidate))
                self.assertEqual(code, 1, result)
                self.assertTrue(
                    any("unsupported host-state sentence" in item for item in result["errors"]),
                    result,
                )


if __name__ == "__main__":
    unittest.main()
