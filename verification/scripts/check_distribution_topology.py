"""Validate Codex plugin closure and a portable Claude/generic skill copy."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from _static_check import default_repo, emit, read_json, read_text, relative, text_files


SKILL_NAME = "impactful-tom"
REFERENCE_PATTERN = re.compile(r"(?<![\w.-])((?:references|assets)/[A-Za-z0-9][A-Za-z0-9._/-]*)")


def parse_frontmatter(skill_path: Path, errors: list[str]) -> dict[str, str]:
    content = read_text(skill_path, errors)
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"SKILL.md lacks opening YAML frontmatter: {skill_path}")
        return {}
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        errors.append(f"SKILL.md lacks closing YAML frontmatter: {skill_path}")
        return {}
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    if values.get("name") != SKILL_NAME:
        errors.append(f"SKILL frontmatter name must be '{SKILL_NAME}'")
    description = values.get("description", "")
    if not description or "TODO" in description.upper():
        errors.append("SKILL frontmatter description is missing or unfinished")
    return values


def validate_references(skill_root: Path, errors: list[str]) -> None:
    for path in text_files(skill_root):
        content = read_text(path, errors)
        for raw_path in REFERENCE_PATTERN.findall(content):
            candidate = (skill_root / raw_path).resolve()
            try:
                candidate.relative_to(skill_root.resolve())
            except ValueError:
                errors.append(f"reference escapes skill root in {relative(path, skill_root)}: {raw_path}")
                continue
            if not candidate.exists():
                errors.append(f"missing runtime resource in {relative(path, skill_root)}: {raw_path}")


def validate_openai_yaml(path: Path, errors: list[str]) -> None:
    content = read_text(path, errors)
    for key in ("display_name", "short_description", "default_prompt"):
        if not re.search(rf"^\s*{key}:\s*['\"].+['\"]\s*$", content, flags=re.MULTILINE):
            errors.append(f"agents/openai.yaml lacks a quoted {key}")
    if "$impactful-tom" not in content:
        errors.append("agents/openai.yaml default prompt does not invoke $impactful-tom")


def portable_files(root: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and "agents" not in path.relative_to(root).parts:
            files[path.relative_to(root).as_posix()] = path.read_bytes()
    return files


def validate_claude_copy(canonical: Path, claude_root: Path, errors: list[str]) -> None:
    if not claude_root.is_dir():
        errors.append(f"Claude/generic skill root is missing: {claude_root}")
        return
    if not (claude_root / "SKILL.md").is_file():
        errors.append(f"Claude/generic skill lacks SKILL.md: {claude_root}")
        return
    expected = portable_files(canonical)
    actual = portable_files(claude_root)
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed = sorted(name for name in set(expected) & set(actual) if expected[name] != actual[name])
    if missing:
        errors.append(f"Claude/generic skill is missing canonical files: {', '.join(missing)}")
    if extra:
        errors.append(f"Claude/generic skill has unexpected files: {', '.join(extra)}")
    if changed:
        errors.append(f"Claude/generic skill differs from canonical files: {', '.join(changed)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=default_repo(__file__))
    parser.add_argument("--claude-root", type=Path)
    parser.add_argument("--require-claude", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    marketplace = read_json(repo / ".agents" / "plugins" / "marketplace.json", errors, "marketplace manifest")
    entries = marketplace.get("plugins", []) if isinstance(marketplace.get("plugins", []), list) else []
    entry = next((item for item in entries if isinstance(item, dict) and item.get("name") == SKILL_NAME), None)
    if entry is None:
        errors.append("marketplace manifest lacks impactful-tom plugin entry")
    else:
        source = entry.get("source", {})
        if not isinstance(source, dict) or source.get("path") != "./plugins/impactful-tom":
            errors.append("marketplace source path must be ./plugins/impactful-tom")
        policy = entry.get("policy", {})
        if not isinstance(policy, dict) or policy.get("installation") != "AVAILABLE":
            errors.append("marketplace policy must expose installation AVAILABLE")

    plugin_root = repo / "plugins" / SKILL_NAME
    plugin = read_json(plugin_root / ".codex-plugin" / "plugin.json", errors, "plugin manifest")
    if plugin.get("name") != SKILL_NAME:
        errors.append("plugin manifest name must be impactful-tom")
    if plugin.get("version") != "1.0.0":
        errors.append("plugin manifest version must be 1.0.0 for the sole public initial release")
    if plugin.get("skills") != "./skills/":
        errors.append("plugin manifest skills path must be ./skills/")

    skill_root = plugin_root / "skills" / SKILL_NAME
    skill_path = skill_root / "SKILL.md"
    if not skill_path.is_file():
        errors.append(f"missing canonical SKILL.md: {skill_path}")
    else:
        parse_frontmatter(skill_path, errors)
        validate_references(skill_root, errors)
    openai_yaml = skill_root / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        errors.append(f"missing Codex interface file: {openai_yaml}")
    else:
        validate_openai_yaml(openai_yaml, errors)
    for directory in ("references", "assets", "evals"):
        path = skill_root / directory
        if not path.is_dir() or not any(path.iterdir()):
            errors.append(f"required runtime directory is missing or empty: {path}")

    if args.claude_root:
        validate_claude_copy(skill_root, args.claude_root.resolve(), errors)
    elif args.require_claude:
        errors.append("--require-claude needs an explicit --claude-root")
    else:
        warnings.append("Claude/generic distribution not checked; rerun with --claude-root and --require-claude")
    return emit("distribution_topology", errors, warnings)


if __name__ == "__main__":
    raise SystemExit(main())
