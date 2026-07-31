#!/usr/bin/env python3
"""Replay one independently captured collaboration judgment into TestForge."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode-dir", type=Path, required=True)
    args = parser.parse_args()

    # Consume the canonical TestForge judge prompt supplied on standard input.
    # The independently captured judgment is already bound to that prompt by
    # judge-batch-receipt.json; TestForge performs its own shape and case checks.
    sys.stdin.read()
    judgment_path = args.episode_dir.resolve() / "manual-judgment.json"
    try:
        judgment = json.loads(judgment_path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"cannot replay judgment: {error}", file=sys.stderr)
        return 2
    if not isinstance(judgment, dict):
        print("cannot replay judgment: JSON root must be an object", file=sys.stderr)
        return 2
    print(json.dumps(judgment, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
