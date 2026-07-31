"""Shared, dependency-free helpers for release-candidate static checks."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable


TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json"}


def default_repo(script_file: str) -> Path:
    return Path(script_file).resolve().parents[2]


def read_json(path: Path, errors: list[str], label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing {label}: {path}")
        return {}
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid {label}: {path} ({exc})")
        return {}
    if not isinstance(value, dict):
        errors.append(f"invalid {label}: expected a JSON object at {path}")
        return {}
    return value


def text_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return (
        path
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
    )


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"text file is not UTF-8: {path}")
    except OSError as exc:
        errors.append(f"cannot read {path}: {exc}")
    return ""


def relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def emit(check: str, errors: list[str], warnings: list[str] | None = None) -> int:
    result = {
        "check": check,
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "warnings": warnings or [],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


def require_text_markers(text: str, markers: Iterable[str], errors: list[str], label: str) -> None:
    lower_text = text.lower()
    for marker in markers:
        if marker.lower() not in lower_text:
            errors.append(f"missing required policy marker '{marker}' in {label}")
