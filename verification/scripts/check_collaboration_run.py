"""Validate hash-bound subject and judge custody for a collaboration eval run."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from _static_check import emit, read_json


SUBJECT_FORMAT = "cd-collaboration-subject-execution/v1"
JUDGE_FORMAT = "cd-collaboration-judge-batch/v1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_record(
    run: Path,
    episode: Path,
    record: dict,
    key: str,
    filename: str,
    errors: list[str],
) -> None:
    case_id = episode.parent.name
    value = record.get(key)
    if not isinstance(value, dict):
        errors.append(f"{case_id}: subject receipt lacks {key} record")
        return
    expected_relative = (episode / filename).relative_to(run).as_posix()
    if value.get("relative_path") != expected_relative:
        errors.append(
            f"{case_id}: {key} path must be {expected_relative}, got {value.get('relative_path')!r}"
        )
    path = run / expected_relative
    if not path.is_file():
        errors.append(f"{case_id}: missing {key} artifact {expected_relative}")
        return
    observed = sha256(path)
    if value.get("sha256") != observed:
        errors.append(f"{case_id}: {key} SHA-256 differs from {expected_relative}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--require-judgments", action="store_true")
    args = parser.parse_args()
    run_root = args.run.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    run_state = read_json(run_root / "run.json", errors, "run state")
    run_id = run_state.get("run_id")
    fingerprint = run_state.get("package_fingerprint_sha256")
    expected = run_state.get("expected_episodes")
    episodes = sorted((run_root / "episodes").glob("*/trial-*"))
    if expected != len(episodes):
        errors.append(f"episode count differs: run expects {expected}, found {len(episodes)}")

    for episode in episodes:
        case_id = episode.parent.name
        trial_text = episode.name.removeprefix("trial-")
        trial = int(trial_text) if trial_text.isdigit() else None
        receipt = read_json(
            episode / "subject-execution.json", errors, f"{case_id} subject receipt"
        )
        if receipt.get("format") != SUBJECT_FORMAT:
            errors.append(f"{case_id}: subject receipt format must be {SUBJECT_FORMAT}")
        if receipt.get("run_id") != run_id:
            errors.append(f"{case_id}: subject receipt run_id differs")
        if receipt.get("case_id") != case_id:
            errors.append(f"{case_id}: subject receipt case_id differs")
        if receipt.get("trial") != trial:
            errors.append(f"{case_id}: subject receipt trial differs")
        if receipt.get("status") != "COMPLETED":
            errors.append(f"{case_id}: subject receipt status is not COMPLETED")
        if receipt.get("package_fingerprint_sha256") != fingerprint:
            errors.append(f"{case_id}: subject receipt package fingerprint differs")
        for key, filename in (
            ("prompt", "subject-prompt.md"),
            ("request", "subject-request.json"),
            ("response", "subject-response.md"),
        ):
            validate_record(run_root, episode, receipt, key, filename, errors)

    state_fixture = (
        run_root
        / "episodes"
        / "S-STATE-002"
        / "trial-001"
        / "evaluator-fixture"
        / "founder-case.md"
    )
    if state_fixture.exists():
        errors.append("S-STATE-002: Founder Case was written without final authorization")

    batch_path = run_root / "judge-batch-receipt.json"
    if batch_path.is_file():
        batch = read_json(batch_path, errors, "judge batch receipt")
        if batch.get("format") != JUDGE_FORMAT:
            errors.append(f"judge batch receipt format must be {JUDGE_FORMAT}")
        if batch.get("run_id") != run_id:
            errors.append("judge batch receipt run_id differs")
        records = batch.get("cases")
        if not isinstance(records, list) or len(records) != len(episodes):
            errors.append("judge batch receipt must cover every episode exactly once")
            records = []
        indexed = {
            item.get("case_id"): item for item in records if isinstance(item, dict)
        }
        if len(indexed) != len(records):
            errors.append("judge batch receipt case IDs must be unique")
        for episode in episodes:
            case_id = episode.parent.name
            item = indexed.get(case_id)
            if not isinstance(item, dict):
                errors.append(f"{case_id}: missing judge batch record")
                continue
            hash_map = item.get("sha256")
            hash_map = hash_map if isinstance(hash_map, dict) else {}
            for field, filename in (
                ("judge_prompt_sha256", "judge-prompt.md"),
                ("subject_response_sha256", "subject-response.md"),
                ("evaluator_rubric_sha256", "evaluator-rubric.json"),
                ("manual_judgment_sha256", "manual-judgment.json"),
            ):
                path = episode / filename
                if not path.is_file():
                    errors.append(f"{case_id}: missing {filename}")
                elif item.get(field, hash_map.get(filename)) != sha256(path):
                    errors.append(f"{case_id}: {field} differs")
    elif args.require_judgments:
        errors.append("judge-batch-receipt.json is required")
    else:
        warnings.append("judge batch receipt not checked; rerun with --require-judgments")

    return emit("collaboration_run_custody", errors, warnings)


if __name__ == "__main__":
    raise SystemExit(main())
