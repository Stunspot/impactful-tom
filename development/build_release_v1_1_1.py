"""Build the frozen Impactful Tom 1.1.1 release stage and deterministic archives."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.1.1"
STAGE = ROOT / "release" / "stage" / f"impactful-tom-v{VERSION}"
ASSETS = ROOT / "release" / "assets" / f"v{VERSION}"
FIXED_TIME = (2026, 7, 31, 12, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def records(root: Path, *, exclude_manifest: bool = False) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        if exclude_manifest and relative == "RELEASE-MANIFEST.json":
            continue
        items.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})
    return items


def tree_digest(items: list[dict[str, object]]) -> str:
    digest = hashlib.sha256()
    for item in items:
        digest.update(str(item["path"]).encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(str(item["sha256"])))
    return digest.hexdigest()


def write_zip(source: Path, destination: Path, top_level: str) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(item for item in source.rglob("*") if item.is_file()):
            relative = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(f"{top_level}/{relative}", FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> int:
    replace_generated = sys.argv[1:] == ["--replace-generated"]
    if sys.argv[1:] and not replace_generated:
        raise SystemExit("usage: build_release_v1_1_1.py [--replace-generated]")

    existing = [path for path in [STAGE, ASSETS] if path.exists()]
    if existing and not replace_generated:
        raise SystemExit("refusing to overwrite an existing 1.1.1 stage or asset directory")
    for path in existing:
        resolved = path.resolve()
        expected_parent = (ROOT / "release").resolve()
        if resolved == expected_parent or expected_parent not in resolved.parents:
            raise SystemExit(f"refusing generated cleanup outside release root: {resolved}")
        shutil.rmtree(resolved)

    STAGE.mkdir(parents=True)
    ASSETS.mkdir(parents=True)

    for directory in [".agents", "dist", "docs", "plugins"]:
        shutil.copytree(ROOT / directory, STAGE / directory)
    for filename in [
        "ATTRIBUTION.md",
        "CHANGELOG.md",
        "DATA-AND-PRIVACY.md",
        "documentation-manifest.json",
        "LICENSE.md",
        "NOTICE.md",
        "README.md",
        "SECURITY.md",
        "SUPPORT.md",
        "TERMS-OF-USE.md",
        "TRADEMARKS.md",
    ]:
        shutil.copy2(ROOT / filename, STAGE / filename)

    stage_records = records(STAGE, exclude_manifest=True)
    manifest = {
        "format": "cd-augment-release-manifest/v1",
        "product": "Impactful Tom",
        "version": VERSION,
        "manifest_scope": "All release files except RELEASE-MANIFEST.json itself",
        "file_count": len(stage_records),
        "tree_sha256": tree_digest(stage_records),
        "files": stage_records,
    }
    (STAGE / "RELEASE-MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    archive_specs = [
        (STAGE, ASSETS / f"impactful-tom-v{VERSION}.zip", f"impactful-tom-v{VERSION}"),
        (
            ROOT / "plugins" / "impactful-tom",
            ASSETS / f"impactful-tom-v{VERSION}-codex-plugin.zip",
            "impactful-tom",
        ),
        (
            ROOT / "plugins" / "impactful-tom" / "skills" / "impactful-tom",
            ASSETS / f"impactful-tom-v{VERSION}-standalone-skill.zip",
            "impactful-tom",
        ),
        (
            ROOT / "dist" / "claude-code" / "impactful-tom",
            ASSETS / f"impactful-tom-v{VERSION}-claude-code-generic-skill.zip",
            "impactful-tom",
        ),
    ]
    for source, destination, top_level in archive_specs:
        write_zip(source, destination, top_level)

    checksum_lines = [
        f"{sha256(destination)}  {destination.name}"
        for _, destination, _ in sorted(archive_specs, key=lambda item: item[1].name)
    ]
    (ASSETS / "SHA256SUMS.txt").write_text(
        "\n".join(checksum_lines) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"stage": str(STAGE), "files": len(stage_records), "assets": len(archive_specs)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
