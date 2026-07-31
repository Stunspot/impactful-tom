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

    def test_distribution_topology_accepts_consistent_semver(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            candidate = Path(temp) / "repo"
            shutil.copytree(FIXTURES / "valid-repo", candidate)
            claude_root = Path(temp) / "claude"
            shutil.copytree(FIXTURES / "valid-claude", claude_root)
            version = "1.2.3"
            for path_text, key in [
                ("plugins/impactful-tom/.codex-plugin/plugin.json", "version"),
                ("plugins/impactful-tom/skills/impactful-tom/package-manifest.yaml", "version"),
                ("plugins/impactful-tom/skills/impactful-tom/evals/eval-manifest.yaml", "package_version"),
            ]:
                path = candidate / path_text
                payload = json.loads(path.read_text(encoding="utf-8"))
                payload[key] = version
                path.write_text(json.dumps(payload), encoding="utf-8")
            for path_text, key in [
                ("package-manifest.yaml", "version"),
                ("evals/eval-manifest.yaml", "package_version"),
            ]:
                path = claude_root / path_text
                payload = json.loads(path.read_text(encoding="utf-8"))
                payload[key] = version
                path.write_text(json.dumps(payload), encoding="utf-8")
            code, result = run(
                "check_distribution_topology.py",
                "--repo",
                str(candidate),
                "--claude-root",
                str(claude_root),
                "--require-claude",
            )
            self.assertEqual(code, 0, result)

    def test_distribution_topology_rejects_version_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            candidate = Path(temp) / "repo"
            shutil.copytree(FIXTURES / "valid-repo", candidate)
            claude_root = Path(temp) / "claude"
            shutil.copytree(FIXTURES / "valid-claude", claude_root)
            manifest_path = claude_root / "evals/eval-manifest.yaml"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["package_version"] = "1.0.1"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            code, result = run(
                "check_distribution_topology.py",
                "--repo",
                str(candidate),
                "--claude-root",
                str(claude_root),
                "--require-claude",
            )
            self.assertEqual(code, 1, result)
            self.assertIn(
                "Claude/generic eval manifest package_version must match plugin version 1.0.0",
                result["errors"],
            )

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

    def test_documentation_release_marker_tracks_manifest_version(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            candidate = Path(temp)
            copy_documentation_fixture(candidate)
            manifest_path = candidate / "documentation-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["product"]["version"] = "1.2.3"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            code, result = run("check_documentation_site.py", "--repo", str(candidate))
            self.assertEqual(code, 1, result)
            self.assertTrue(
                any(
                    "README missing public presentation marker: "
                    "https://github.com/Stunspot/impactful-tom/releases/tag/v1.2.3" in item
                    for item in result["errors"]
                ),
                result,
            )


if __name__ == "__main__":
    unittest.main()
