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
        "development/documentation-project.json",
        "plugins/impactful-tom/assets/founder-constraint-mark.png",
        "verification/documentation/documentation-authorship.json",
        "verification/documentation/documentation-review.json",
        "verification/documentation/hesperos-pages-authoring-evidence.md",
        "verification/documentation/hesperos-pages-authoring-response.txt",
        "verification/documentation/visual-assets-custody.json",
        "verification/live-verification.json",
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

    def test_content_gate_rejects_warning_label_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            candidate = Path(temp) / "repo"
            shutil.copytree(FIXTURES / "valid-repo", candidate)
            skill = (
                candidate
                / "plugins"
                / "impactful-tom"
                / "skills"
                / "impactful-tom"
                / "SKILL.md"
            )
            skill.write_text(
                skill.read_text(encoding="utf-8")
                + "\nThis is an unofficial machine impression and is not affiliated.\n",
                encoding="utf-8",
            )
            code, result = run("check_content_boundaries.py", "--repo", str(candidate))
            self.assertEqual(code, 1, result)
            self.assertTrue(
                any("customer runtime experience" in item for item in result["errors"]),
                result,
            )

    def test_documentation_gate_rejects_warning_first_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            candidate = Path(temp)
            copy_documentation_fixture(candidate)
            readme = candidate / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8")
                + "\n\nThis is an unofficial machine impression and is not affiliated.\n",
                encoding="utf-8",
            )
            code, result = run("check_documentation_site.py", "--repo", str(candidate))
            self.assertEqual(code, 1, result)
            self.assertTrue(
                any("warning-label language" in item for item in result["errors"]),
                result,
            )

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

    def test_live_visual_claim_variants_require_matching_receipt_lineage(self) -> None:
        escaped_cycle_one = (
            "On 2026-08-11, direct public readback confirmed the repository, release, "
            "all five release assets, six Pages routes, 21 customer-journey links, "
            "the three role-specific visual assets, and the custom GitHub social preview."
        )
        wrapped_cycle_one = escaped_cycle_one.replace(
            "repository, release,",
            "repository,\n  release,",
        )
        claims = [
            escaped_cycle_one,
            wrapped_cycle_one,
            "Public readback confirmed the redesigned README hero and social card.",
            "The latest visual presentation is published with exact deployed asset parity.",
        ]
        surfaces = {
            "README.md": (
                "Clean public-route installation",
                "{claim}\n\nClean public-route installation",
            ),
            "CHANGELOG.md": (
                "- Classified the [2026-08-11 live-verification receipt]",
                "- {claim}\n- Classified the [2026-08-11 live-verification receipt]",
            ),
            "docs/provenance-and-verification.md": (
                "## How to read release claims",
                "{claim}\n\n## How to read release claims",
            ),
        }
        for path_text, (marker, replacement) in surfaces.items():
            for claim in claims:
                with self.subTest(path=path_text, claim=claim), tempfile.TemporaryDirectory() as temp:
                    candidate = Path(temp)
                    copy_documentation_fixture(candidate)
                    path = candidate / path_text
                    text = path.read_text(encoding="utf-8")
                    self.assertIn(marker, text)
                    path.write_text(
                        text.replace(marker, replacement.format(claim=claim), 1),
                        encoding="utf-8",
                    )
                    code, result = run("check_documentation_site.py", "--repo", str(candidate))
                    self.assertEqual(code, 1, result)
                    self.assertTrue(
                        any(
                            "current live presentation claim lacks matching receipt lineage" in item
                            for item in result["errors"]
                        ),
                        result,
                    )

    def test_contradictory_live_claim_inside_historical_item_is_rejected(self) -> None:
        contradictions = [
            " The current replacement visual presentation is live and deployed.",
            "; The current replacement visual presentation is live and deployed.",
        ]
        surfaces = {
            "README.md": "Earlier release tags remain historical custody and are not rewritten.",
            "CHANGELOG.md": "its recorded role-image hashes do not verify the replacement hero, social card, or palette.",
            "docs/provenance-and-verification.md": "Public availability does not establish host installation or invocation.",
        }
        for path_text, marker in surfaces.items():
            for contradiction in contradictions:
                with self.subTest(path=path_text, contradiction=contradiction), tempfile.TemporaryDirectory() as temp:
                    candidate = Path(temp)
                    copy_documentation_fixture(candidate)
                    path = candidate / path_text
                    text = path.read_text(encoding="utf-8")
                    self.assertIn(marker, text)
                    path.write_text(
                        text.replace(marker, marker + contradiction, 1),
                        encoding="utf-8",
                    )
                    code, result = run("check_documentation_site.py", "--repo", str(candidate))
                    self.assertEqual(code, 1, result)
                    self.assertTrue(
                        any(
                            "current live presentation claim lacks matching receipt lineage" in item
                            for item in result["errors"]
                        ),
                        result,
                    )
    def test_dated_replacement_claim_inside_historical_item_is_rejected(self) -> None:
        contradictions = [
            " On 2026-08-11, public readback confirmed this remediation's replacement social card is live.",
            "; On 2026-08-11, public readback confirmed this remediation's replacement social card is live.",
        ]
        surfaces = {
            "README.md": "Earlier release tags remain historical custody and are not rewritten.",
            "CHANGELOG.md": "its recorded role-image hashes do not verify the replacement hero, social card, or palette.",
            "docs/provenance-and-verification.md": "Public availability does not establish host installation or invocation.",
        }
        for path_text, marker in surfaces.items():
            for contradiction in contradictions:
                with self.subTest(path=path_text, contradiction=contradiction), tempfile.TemporaryDirectory() as temp:
                    candidate = Path(temp)
                    copy_documentation_fixture(candidate)
                    path = candidate / path_text
                    text = path.read_text(encoding="utf-8")
                    self.assertIn(marker, text)
                    path.write_text(
                        text.replace(marker, marker + contradiction, 1),
                        encoding="utf-8",
                    )
                    code, result = run("check_documentation_site.py", "--repo", str(candidate))
                    self.assertEqual(code, 1, result)
                    self.assertTrue(
                        any(
                            "current live presentation claim lacks matching receipt lineage" in item
                            for item in result["errors"]
                        ),
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
