"""Check that the public runtime is product-first and keeps legal facts centralized."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from _static_check import default_repo, emit, read_text, text_files


FORBIDDEN_PATTERNS = {
    "deceptive literal identity": r"(?m)^\s*(?:you are|i am)\s+tom\s+bilyeu\b",
    "authentic-speech claim": r"(?mi)^(?!.*\b(?:never|do not|don't|not)\b).*\btom\s+bilyeu['’]s\s+(?:authentic\s+)?(?:words|advice|statement)\b",
    "official affiliation claim": r"\bimpact\s+theory\s+(?:official|approved|endorsed)\b",
    "automatic analytics claim": r"\bautomatic(?:ally)?\s+analytics\b",
    "automatic persistence claim": r"\bautomatic(?:ally)?\s+(?:save|saved|store|stored|persist|persisted)\b",
}

REQUIRED_PATTERNS = {
    "founder-performance product": (
        r"\bfounder[ -]performance\b",
        r"\baugment\b",
    ),
    "distinctive performance profile": (
        r"\bperformance profile\b",
        r"\b(?:cadence|consequence framing|explanatory pressure)\b",
    ),
    "quiet identity boundary": (
        r"\bidentity is directly asked\b",
        r"\breturn immediately\b.{0,120}\bfounder",
    ),
    "fabricated attribution boundary": (
        r"\b(?:deceptive attribution|invent a quote|original lines stay unattributed)\b",
    ),
    "session-first state": (
        r"\bsession(?:-only|\s+only)\b",
        r"\bfounder\s+case\b",
        r"\bexplicit(?:ly)?\b",
    ),
    "optional MIND boundary": (
        r"\bmind\b",
        r"(?:\boptional\b|\bwhen\b.{0,40}\bavailable\b|\bmay\s+supply\b)",
    ),
    "separate external-action authority": (
        r"\bseparat(?:e|ely)\s+authoriz",
    ),
}

EXPERIENCE_FORBIDDEN_PATTERNS = {
    "proper-name reference": r"\b(?:tom\s+bilyeu|impact\s+theory)\b",
    "construction-first framing": r"\bmachine[ -]impression\b",
    "warning-label status": r"\bunofficial\b|\bnot\s+affiliat",
    "legal theory in runtime experience": r"\bparod(?:y|ic)\b|\bfair\s+use\b",
}

NOTICE_REQUIRED_PATTERNS = {
    "centralized product identity": r"\bimpactful tom is a collaborative dynamics augment\b",
    "independent production": r"\bindependently produced\b",
    "third-party official-status boundary": r"\bnot an official or endorsed product of any third party\b",
    "generated-output boundary": r"\bgenerates its own output\b",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=default_repo(__file__))
    parser.add_argument("--skill-root", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    skill_root = (args.skill_root or repo / "plugins" / "impactful-tom" / "skills" / "impactful-tom").resolve()
    errors: list[str] = []

    files = [
        path
        for path in text_files(skill_root)
        if "evals" not in path.relative_to(skill_root).parts
    ]
    if not files:
        errors.append(f"no runtime text files found below {skill_root}")
        return emit("content_boundaries", errors)

    corpus_parts: list[str] = []
    for path in files:
        content = read_text(path, errors)
        corpus_parts.append(content)
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if re.search(pattern, content, flags=re.IGNORECASE):
                errors.append(f"{label} found in {path.relative_to(skill_root).as_posix()}")
        if "[TODO" in content or "TODO:" in content:
            errors.append(f"unfinished scaffold marker found in {path.relative_to(skill_root).as_posix()}")

        relative_path = path.relative_to(skill_root)
        if relative_path.name == "SKILL.md" or (
            relative_path.parts and relative_path.parts[0] == "references"
        ):
            for label, pattern in EXPERIENCE_FORBIDDEN_PATTERNS.items():
                if re.search(pattern, content, flags=re.IGNORECASE):
                    errors.append(
                        f"{label} found in customer runtime experience "
                        f"{relative_path.as_posix()}"
                    )

    corpus = "\n".join(corpus_parts).lower()
    for label, patterns in REQUIRED_PATTERNS.items():
        if not all(re.search(pattern, corpus, flags=re.IGNORECASE | re.DOTALL) for pattern in patterns):
            errors.append(f"missing {label} policy language")

    notice = read_text(skill_root / "NOTICE.md", errors)
    for label, pattern in NOTICE_REQUIRED_PATTERNS.items():
        if not re.search(pattern, notice, flags=re.IGNORECASE):
            errors.append(f"NOTICE.md missing {label} language")
    return emit("content_boundaries", errors)


if __name__ == "__main__":
    raise SystemExit(main())
