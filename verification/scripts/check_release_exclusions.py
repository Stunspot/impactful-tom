"""Reject private canonical-source traces from publishable release surfaces.

This is a filename/hash/marker boundary check, not a plagiarism detector. It
does not establish independent authorship or a third-party rights basis.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from _static_check import default_repo, emit, read_json, relative


PUBLISHABLE_DEFAULTS = (".agents", "plugins", "README.md", "docs", "dist", "release")
KNOWN_PRIVATE_MARKERS = (
    ":contentReference[oaicite",
    "cosine-tuned",
    "knowledge engineering protocol",
)
PRIVATE_PATH_MARKERS = ("e:\\indranet\\", "e:/indranet/")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def selected_roots(repo: Path, surfaces: list[str]) -> list[Path]:
    roots = []
    for surface in surfaces:
        candidate = repo / surface
        if candidate.exists():
            roots.append(candidate)
    return roots


def iter_files(root: Path):
    if root.is_file():
        yield root
        return
    yield from (path for path in sorted(root.rglob("*")) if path.is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=default_repo(__file__))
    parser.add_argument(
        "--surface",
        action="append",
        dest="surfaces",
        help="repo-relative publishable surface; repeat to override defaults",
    )
    args = parser.parse_args()
    repo = args.repo.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    custody = read_json(repo / "verification" / "source-custody.json", errors, "source custody")
    sources = custody.get("sources", []) if isinstance(custody.get("sources", []), list) else []
    excluded_names = {
        item.get("name", "").lower()
        for item in sources
        if isinstance(item, dict) and item.get("state") in {"release-excluded-private", "build-only", "consulted-build-only"}
    }
    excluded_hashes = {
        item.get("sha256", "").upper()
        for item in sources
        if isinstance(item, dict) and item.get("sha256")
    }
    if not excluded_names or not excluded_hashes:
        errors.append("source custody does not provide excluded source names and hashes")

    surfaces = args.surfaces or list(PUBLISHABLE_DEFAULTS)
    roots = selected_roots(repo, surfaces)
    if not roots:
        errors.append("no publishable surfaces found; pass --surface for an explicit candidate")

    for root in roots:
        for path in iter_files(root):
            display = relative(path, repo)
            if path.name.lower() in excluded_names:
                errors.append(f"release-excluded source filename present: {display}")
            try:
                digest = file_hash(path)
            except OSError as exc:
                errors.append(f"cannot hash {display}: {exc}")
                continue
            if digest in excluded_hashes:
                errors.append(f"release-excluded source bytes present: {display}")
            if path.suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".json"}:
                try:
                    content = path.read_text(encoding="utf-8").lower()
                except (OSError, UnicodeDecodeError) as exc:
                    errors.append(f"cannot inspect text {display}: {exc}")
                    continue
                for marker in KNOWN_PRIVATE_MARKERS:
                    if marker in content:
                        errors.append(f"private corpus marker '{marker}' in {display}")
                for marker in PRIVATE_PATH_MARKERS:
                    if marker in content:
                        errors.append(f"private local path marker in {display}")

    if not (repo / "dist").exists() and not (repo / "release").exists():
        warnings.append("archive/release surface is not present; only repository publishable surfaces were scanned")
    return emit("release_exclusions", errors, warnings)


if __name__ == "__main__":
    raise SystemExit(main())
