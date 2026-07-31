"""Dependency-free verification for the public Impactful Tom documentation site."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
from urllib.parse import urlsplit

from _static_check import emit, read_text, relative


EXPECTED_ORIGIN = "https://stunspot.github.io"
EXPECTED_BASEURL = "/impactful-tom"
EXPECTED_ROOT = f"{EXPECTED_ORIGIN}{EXPECTED_BASEURL}/"
EXPECTED_SOURCE_MARK_SHA256 = (
    "684e4d435fb213e6806cf0cbc362e7f33300ba2e2346d5445dd8d3b72c859773"
)

REQUIRED_TEXT_FILES = [
    "README.md",
    "docs/_config.yml",
    "docs/_layouts/default.html",
    "docs/assets/css/site.css",
    "docs/index.md",
    "docs/404.html",
    "docs/getting-started.md",
    "docs/installing-and-maintaining.md",
    "docs/privacy-and-boundaries.md",
    "docs/provenance-and-verification.md",
    "docs/troubleshooting.md",
    "docs/site.webmanifest",
    "documentation-manifest.json",
    "verification/documentation/documentation-authorship.json",
    "verification/documentation/documentation-review.json",
    "verification/documentation/visual-assets-custody.json",
]

PAGE_FILES = [
    "docs/index.md",
    "docs/getting-started.md",
    "docs/installing-and-maintaining.md",
    "docs/privacy-and-boundaries.md",
    "docs/provenance-and-verification.md",
    "docs/troubleshooting.md",
    "docs/404.html",
]

PNG_CONTRACTS = {
    "docs/assets/images/impactful-tom-header.png": (1600, 500, 1_000_000),
    "docs/assets/images/impactful-tom-social-card.png": (1280, 640, 1_000_000),
    "docs/assets/images/impactful-tom-mark-512.png": (512, 512, 500_000),
    "docs/assets/images/impactful-tom-mark-192.png": (192, 192, 150_000),
    "docs/assets/images/apple-touch-icon.png": (180, 180, 150_000),
    "docs/assets/images/favicon-48.png": (48, 48, 25_000),
    "docs/assets/images/favicon-32.png": (32, 32, 25_000),
    "docs/assets/images/favicon-16.png": (16, 16, 10_000),
}

STALE_PATTERNS = {
    "prepared for publication": re.compile(r"\bprepared for publication\b", re.I),
    "prepared for one public release": re.compile(r"\bprepared for one public\b", re.I),
    "no public GitHub repository": re.compile(r"\bno public GitHub repository\b", re.I),
    "not yet public": re.compile(r"\bnot yet public\b", re.I),
    "release assets pending publication": re.compile(
        r"\brelease[- ]asset(?: readback)?[^.\n]{0,80}\bpending\b", re.I
    ),
    "repository not created": re.compile(r"\brepository[^.\n]{0,40}\bnot[- ]created\b", re.I),
}

PUBLIC_CLAIM_FILES = [
    "README.md",
    "CHANGELOG.md",
    "SUPPORT.md",
    "SECURITY.md",
    *PAGE_FILES,
]

BOUNDED_HOST_CLAIMS = {
    "README.md": {
        "combined public-route host limits": re.compile(
            r"\bclean public-route installation[^.\n]{0,240}\bremain unobserved\b",
            re.I,
        )
    },
    "docs/installing-and-maintaining.md": {
        "clean public-route installation": re.compile(
            r"\bexact final package has not been installed[^.\n]{0,120}\bclean public route\b",
            re.I,
        ),
        "restart resilience": re.compile(
            r"\brestart resilience[^.\n]{0,120}\bremain unobserved\b", re.I
        ),
        "causal host invocation": re.compile(
            r"\bcausal host invocation[^.\n]{0,120}\bremain unobserved\b", re.I
        ),
        "Claude live-host behavior": re.compile(
            r"\bClaude Code/generic skill directory[^.\n]{0,160}\bwithout live-host evidence\b",
            re.I,
        ),
    },
    "docs/provenance-and-verification.md": {
        "clean public-route installation": re.compile(
            r"\bno clean public-route installation receipt[^.\n]{0,140}\bhas been observed\b",
            re.I,
        ),
        "restart resilience": re.compile(
            r"\brestart resilience has not been observed\b", re.I
        ),
        "causal host invocation": re.compile(
            r"\bcausal host invocation[^.\n]{0,100}\bhas not been observed\b", re.I
        ),
        "Claude live-host behavior": re.compile(
            r"\bClaude Code live installation[^.\n]{0,180}\bhave not been observed\b",
            re.I,
        ),
    },
}

HOST_STATE_SENTENCE_CONTRACTS = {
    "clean public-route installation": {
        "subject": re.compile(
            r"\b(?:clean public-route installation|clean installation|"
            r"clean public-route host|clean public route)\b",
            re.I,
        ),
        "allowed": [
            re.compile(
                r"\bclean public-route installation[^.\n]{0,240}\bremain unobserved\b",
                re.I,
            ),
            re.compile(
                r"\bnot (?:yet )?been installed[^.\n]{0,140}\bclean public-route host\b",
                re.I,
            ),
            re.compile(
                r"\bexact final package has not been installed[^.\n]{0,140}"
                r"\bclean public route\b",
                re.I,
            ),
            re.compile(
                r"\bno clean public-route installation receipt[^.\n]{0,160}"
                r"\bhas been observed\b",
                re.I,
            ),
            re.compile(
                r"\bdo not establish[^.\n]{0,240}\bclean public-route installation\b",
                re.I,
            ),
        ],
    },
    "restart resilience": {
        "subject": re.compile(r"\brestart resilience\b", re.I),
        "allowed": [
            re.compile(
                r"\brestart resilience[^.\n]{0,240}\bremain unobserved\b", re.I
            ),
            re.compile(r"\brestart resilience has not been observed\b", re.I),
            re.compile(
                r"\bdo not establish[^.\n]{0,240}\brestart resilience\b", re.I
            ),
        ],
    },
    "causal host invocation": {
        "subject": re.compile(r"\bcausal host invocation\b", re.I),
        "allowed": [
            re.compile(
                r"\bcausal host invocation[^.\n]{0,240}\bremain unobserved\b", re.I
            ),
            re.compile(
                r"\bcausal host invocation[^.\n]{0,120}\bhas not been observed\b",
                re.I,
            ),
            re.compile(
                r"\bdo not establish[^.\n]{0,240}\bcausal host invocation\b", re.I
            ),
        ],
    },
    "Claude live-host behavior": {
        "subject": re.compile(
            r"\b(?:live Claude Code behavior|Claude Code live behavior|Claude live-host behavior|"
            r"Claude Code/generic skill directory|Claude Code live installation)\b",
            re.I,
        ),
        "allowed": [
            re.compile(
                r"\blive Claude Code behavior[^.\n]{0,180}\bremain unobserved\b",
                re.I,
            ),
            re.compile(
                r"\bClaude live-host behavior[^.\n]{0,120}\bremains unobserved\b",
                re.I,
            ),
            re.compile(
                r"\bClaude Code/generic skill directory[^.\n]{0,180}"
                r"\bwithout live-host evidence\b",
                re.I,
            ),
            re.compile(
                r"\bClaude Code live installation[^.\n]{0,200}"
                r"\bhave not been observed\b",
                re.I,
            ),
            re.compile(
                r"\bdo not establish[^.\n]{0,240}\blive Claude Code behavior\b",
                re.I,
            ),
        ],
    },
}

LIQUID_URL = re.compile(
    r"""\{\{\s*["'](?P<path>[^"']+)["']\s*\|\s*(?P<filter>relative_url|absolute_url)\s*\}\}"""
)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\((?P<target>[^)\n]+)\)")
HTML_LINK = re.compile(
    r"""(?:href|src)=(?P<quote>["'])(?P<target>.*?)(?P=quote)""",
    re.I,
)


def parse_simple_yaml(text: str) -> dict[str, str]:
    """Parse only unindented scalar key/value pairs used by this site."""

    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        if not raw_line or raw_line[0].isspace() or raw_line.lstrip().startswith("#"):
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key:
            values[key] = value
    return values


def parse_front_matter(path: Path, errors: list[str]) -> tuple[dict[str, str], str]:
    text = read_text(path, errors)
    lines = text.splitlines()
    label = path.as_posix()
    if not lines or lines[0].strip() != "---":
        errors.append(f"missing front matter: {label}")
        return {}, text
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        errors.append(f"unterminated front matter: {label}")
        return {}, text
    front_matter = parse_simple_yaml("\n".join(lines[1:end]))
    return front_matter, "\n".join(lines[end + 1 :])


def png_dimensions(path: Path, errors: list[str]) -> tuple[int, int] | None:
    try:
        with path.open("rb") as stream:
            header = stream.read(24)
    except OSError as exc:
        errors.append(f"cannot read PNG {path}: {exc}")
        return None
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        errors.append(f"invalid PNG signature: {path.as_posix()}")
        return None
    if struct.unpack(">I", header[8:12])[0] != 13 or header[12:16] != b"IHDR":
        errors.append(f"invalid PNG IHDR: {path.as_posix()}")
        return None
    return struct.unpack(">II", header[16:24])


def linear_channel(value: int) -> float:
    channel = value / 255
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    normalized = hex_color.lstrip("#")
    red, green, blue = (int(normalized[index : index + 2], 16) for index in (0, 2, 4))
    return (
        0.2126 * linear_channel(red)
        + 0.7152 * linear_channel(green)
        + 0.0722 * linear_channel(blue)
    )


def contrast_ratio(foreground: str, background: str) -> float:
    high, low = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def extract_targets(text: str) -> list[str]:
    targets = [match.group("target").strip() for match in MARKDOWN_LINK.finditer(text)]
    targets.extend(match.group("target").strip() for match in HTML_LINK.finditer(text))
    return targets


def liquid_path(target: str) -> str | None:
    match = LIQUID_URL.fullmatch(target.strip())
    return match.group("path") if match else None


def validate_internal_target(
    *,
    target: str,
    source: Path,
    repo: Path,
    permalink_map: dict[str, Path],
    errors: list[str],
) -> None:
    if not target or target.startswith(("#", "mailto:", "tel:")):
        return

    if target.strip() == "{{ page.url | absolute_url }}":
        return

    liquid_target = liquid_path(target)
    if "{{" in target or "{%" in target:
        if liquid_target is None:
            errors.append(f"unsupported Liquid URL in {relative(source, repo)}: {target}")
            return
        target = liquid_target

    parsed = urlsplit(target)
    if parsed.scheme:
        if parsed.scheme != "https":
            errors.append(f"non-HTTPS public URL in {relative(source, repo)}: {target}")
        if parsed.hostname in {"localhost", "127.0.0.1"}:
            errors.append(f"local-only URL in {relative(source, repo)}: {target}")
        return

    path = parsed.path
    if not path:
        return
    if "\\" in path or re.match(r"^[A-Za-z]:", path):
        errors.append(f"workstation path in {relative(source, repo)}: {target}")
        return
    if ".." in Path(path).parts:
        errors.append(f"parent-directory escape in {relative(source, repo)}: {target}")
        return

    if path.startswith("/"):
        if path.startswith(f"{EXPECTED_BASEURL}/") or path == EXPECTED_BASEURL:
            path = path[len(EXPECTED_BASEURL) :] or "/"
        if path in permalink_map:
            return
        asset_candidate = repo / "docs" / path.lstrip("/")
        if asset_candidate.is_file():
            return
        errors.append(f"unresolved site route in {relative(source, repo)}: {target}")
        return

    candidate = (source.parent / path).resolve()
    try:
        candidate.relative_to(repo.resolve())
    except ValueError:
        errors.append(f"link escapes repository in {relative(source, repo)}: {target}")
        return
    if not candidate.is_file():
        errors.append(f"missing local target in {relative(source, repo)}: {target}")


def check_required_files(repo: Path, errors: list[str]) -> None:
    for path_text in REQUIRED_TEXT_FILES:
        path = repo / path_text
        if not path.is_file():
            errors.append(f"missing documentation surface: {path_text}")
            continue
        read_text(path, errors)


def check_config(repo: Path, errors: list[str]) -> None:
    config_path = repo / "docs/_config.yml"
    config = parse_simple_yaml(read_text(config_path, errors))
    expected = {
        "url": EXPECTED_ORIGIN,
        "baseurl": EXPECTED_BASEURL,
        "title": "Impactful Tom",
    }
    for key, value in expected.items():
        if config.get(key) != value:
            errors.append(f"docs/_config.yml must set {key}: {value}")
    if not config.get("description"):
        errors.append("docs/_config.yml must set a description")


def check_pages(repo: Path, errors: list[str]) -> dict[str, Path]:
    permalink_map: dict[str, Path] = {}
    for path_text in PAGE_FILES:
        path = repo / path_text
        if not path.is_file():
            continue
        front_matter, body = parse_front_matter(path, errors)
        for key in ("layout", "title", "description", "permalink"):
            if not front_matter.get(key):
                errors.append(f"{path_text} front matter must set {key}")
        permalink = front_matter.get("permalink")
        if permalink:
            if permalink in permalink_map:
                errors.append(
                    f"duplicate permalink {permalink}: {path_text} and "
                    f"{relative(permalink_map[permalink], repo)}"
                )
            permalink_map[permalink] = path
        if front_matter.get("hide_page_title", "").lower() == "true":
            if len(re.findall(r"<h1\b", body, flags=re.I)) != 1:
                errors.append(f"{path_text} must provide exactly one content h1")
        elif re.search(r"^#\s+", body, flags=re.M):
            errors.append(f"{path_text} duplicates the layout-provided h1")

    expected_routes = {
        "/",
        "/getting-started/",
        "/install/",
        "/boundaries/",
        "/evidence/",
        "/troubleshooting/",
        "/404.html",
    }
    missing_routes = sorted(expected_routes - set(permalink_map))
    for route in missing_routes:
        errors.append(f"missing Pages permalink: {route}")
    return permalink_map


def check_layout_and_css(repo: Path, errors: list[str]) -> None:
    layout = read_text(repo / "docs/_layouts/default.html", errors)
    css = read_text(repo / "docs/assets/css/site.css", errors)

    layout_markers = [
        '<a class="skip-link" href="#main-content">',
        '<main id="main-content"',
        'aria-label="Primary navigation"',
        'aria-label="Footer navigation"',
        'rel="canonical"',
        "page.url | absolute_url",
        'property="og:title"',
        'property="og:description"',
        'property="og:url"',
        'property="og:image"',
        'name="twitter:card"',
        "impactful-tom-social-card.png",
        "'/assets/css/site.css' | relative_url",
    ]
    for marker in layout_markers:
        if marker not in layout:
            errors.append(f"layout missing required marker: {marker}")
    if len(re.findall(r"<main\b", layout, flags=re.I)) != 1:
        errors.append("layout must contain exactly one main landmark")
    if '<img src="{{ \'/assets/images/impactful-tom-mark-512.png\' | relative_url }}"' in layout:
        brand_tag = re.search(r"<img[^>]+impactful-tom-mark-512\.png[^>]*>", layout, flags=re.I)
        if brand_tag and ('alt=""' not in brand_tag.group(0) or 'aria-hidden="true"' not in brand_tag.group(0)):
            errors.append("decorative brand image must use empty alt text and aria-hidden=true")

    css_markers = [
        ":focus-visible",
        "@media (max-width:",
        "@media (prefers-reduced-motion: reduce)",
        "outline:",
        "text-underline-offset:",
    ]
    for marker in css_markers:
        if marker not in css:
            errors.append(f"stylesheet missing required marker: {marker}")
    if re.search(r"outline\s*:\s*(?:none|0(?:\D|$))", css, flags=re.I):
        errors.append("stylesheet suppresses focus outlines")
    if "box-shadow: 0 0 0 6px" not in css:
        errors.append("focus treatment must include a two-color outer ring")

    contrast_pairs = [
        ("body text", "#111827", "#f3f6fb", 4.5),
        ("body links", "#00617e", "#f3f6fb", 4.5),
        ("hero copy", "#f4f7ff", "#02071d", 4.5),
        ("hero cyan", "#03bffc", "#02071d", 4.5),
        ("dark-mode links", "#7fe4ff", "#050c22", 4.5),
    ]
    for label, foreground, background, minimum in contrast_pairs:
        ratio = contrast_ratio(foreground, background)
        if ratio < minimum:
            errors.append(f"{label} contrast {ratio:.2f}:1 is below {minimum:.1f}:1")


def check_links(repo: Path, permalink_map: dict[str, Path], errors: list[str]) -> None:
    surfaces = [
        repo / "README.md",
        repo / "CHANGELOG.md",
        repo / "SUPPORT.md",
        repo / "SECURITY.md",
        *[repo / path for path in PAGE_FILES],
        repo / "docs/_layouts/default.html",
    ]
    for source in surfaces:
        if not source.is_file():
            continue
        text = read_text(source, errors)
        for target in extract_targets(text):
            validate_internal_target(
                target=target,
                source=source,
                repo=repo,
                permalink_map=permalink_map,
                errors=errors,
            )


def check_metadata(repo: Path, errors: list[str]) -> None:
    layout = read_text(repo / "docs/_layouts/default.html", errors)
    if "{{ social_image | absolute_url }}" not in layout:
        errors.append("Open Graph image must be emitted through absolute_url")
    if "{{ page.url | absolute_url }}" not in layout:
        errors.append("canonical and Open Graph URLs must use page.url | absolute_url")
    if 'content="1280"' not in layout or 'content="640"' not in layout:
        errors.append("Open Graph image dimensions must declare 1280 by 640")

    manifest_path = repo / "docs/site.webmanifest"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid docs/site.webmanifest: {exc}")
        return
    if manifest.get("start_url") != f"{EXPECTED_BASEURL}/":
        errors.append(f"site.webmanifest start_url must be {EXPECTED_BASEURL}/")
    if manifest.get("scope") != f"{EXPECTED_BASEURL}/":
        errors.append(f"site.webmanifest scope must be {EXPECTED_BASEURL}/")


def check_public_claims(repo: Path, errors: list[str]) -> None:
    combined_parts: list[str] = []
    for path_text in PUBLIC_CLAIM_FILES:
        path = repo / path_text
        if not path.is_file():
            continue
        text = read_text(path, errors)
        combined_parts.append(text)
        for label, pattern in STALE_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"stale publication claim '{label}' in {path_text}")
        segments = [
            segment.strip()
            for segment in re.split(r"(?<=[.!?])\s+|\n+", text)
            if segment.strip()
        ]
        for segment in segments:
            for label, contract in HOST_STATE_SENTENCE_CONTRACTS.items():
                if contract["subject"].search(segment) and not any(
                    pattern.search(segment) for pattern in contract["allowed"]
                ):
                    errors.append(
                        f"unsupported host-state sentence '{label}' in "
                        f"{path_text}: {segment}"
                    )
    combined = "\n".join(combined_parts).lower()
    required_claims = [
        "publicly available",
        "v1.0.0",
        "independent, unofficial",
        "not affiliated",
    ]
    for claim in required_claims:
        if claim not in combined:
            errors.append(f"public documentation missing bounded claim marker: {claim}")
    for path_text, claims in BOUNDED_HOST_CLAIMS.items():
        text = read_text(repo / path_text, errors)
        for label, pattern in claims.items():
            if not pattern.search(text):
                errors.append(f"{path_text} missing explicit unobserved claim: {label}")


def check_accessibility_content(repo: Path, errors: list[str]) -> None:
    surfaces = [repo / path for path in PAGE_FILES] + [repo / "README.md"]
    for path in surfaces:
        if not path.is_file():
            continue
        text = read_text(path, errors)
        if re.search(r"\bclick here\b|\bclick the (?:image|button|link)\b", text, flags=re.I):
            errors.append(f"pointer-only instruction in {relative(path, repo)}")
        for image_tag in re.findall(r"<img\b[^>]*>", text, flags=re.I):
            if not re.search(r"\balt=(?:\"[^\"]*\"|'[^']*')", image_tag, flags=re.I):
                errors.append(f"HTML image missing alt text in {relative(path, repo)}")
            if re.search(r"\balt=(?:\"\"|'')", image_tag, flags=re.I) and not re.search(
                r'\baria-hidden=(?:"true"|\'true\')', image_tag, flags=re.I
            ):
                errors.append(
                    f"decorative HTML image missing aria-hidden=true in {relative(path, repo)}"
                )


def check_pngs(repo: Path, errors: list[str]) -> None:
    for path_text, (expected_width, expected_height, max_bytes) in PNG_CONTRACTS.items():
        path = repo / path_text
        if not path.is_file():
            errors.append(f"missing visual asset: {path_text}")
            continue
        dimensions = png_dimensions(path, errors)
        if dimensions and dimensions != (expected_width, expected_height):
            errors.append(
                f"{path_text} is {dimensions[0]}x{dimensions[1]}, "
                f"expected {expected_width}x{expected_height}"
            )
        size = path.stat().st_size
        if size > max_bytes:
            errors.append(f"{path_text} is {size} bytes, exceeds {max_bytes}")

    source_mark = repo / "plugins/impactful-tom/assets/founder-constraint-mark.png"
    if not source_mark.is_file():
        errors.append("approved source mark is missing")
    else:
        digest = hashlib.sha256(source_mark.read_bytes()).hexdigest()
        if digest != EXPECTED_SOURCE_MARK_SHA256:
            errors.append("approved source mark digest changed without visual-custody update")


def check_visual_custody(repo: Path, errors: list[str]) -> None:
    receipt_path = repo / "verification/documentation/visual-assets-custody.json"
    try:
        receipt = json.loads(read_text(receipt_path, errors))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"invalid visual-assets custody receipt: {exc}")
        return

    source = receipt.get("source", {})
    if source.get("path") != "plugins/impactful-tom/assets/founder-constraint-mark.png":
        errors.append("visual custody receipt names the wrong source mark")
    if source.get("sha256") != EXPECTED_SOURCE_MARK_SHA256:
        errors.append("visual custody receipt has the wrong source-mark digest")

    generator = receipt.get("generator", {})
    generator_path = repo / str(generator.get("path", ""))
    if not generator_path.is_file():
        errors.append("visual custody receipt generator is missing")
    elif hashlib.sha256(generator_path.read_bytes()).hexdigest() != generator.get("sha256"):
        errors.append("visual custody receipt generator digest does not match")

    outputs = {
        item.get("path"): item
        for item in receipt.get("outputs", [])
        if isinstance(item, dict) and item.get("path")
    }
    if set(outputs) != set(PNG_CONTRACTS):
        errors.append("visual custody receipt output set does not match the site PNG contract")
    for path_text, (expected_width, expected_height, _) in PNG_CONTRACTS.items():
        item = outputs.get(path_text)
        path = repo / path_text
        if not item or not path.is_file():
            continue
        if (item.get("width"), item.get("height")) != (expected_width, expected_height):
            errors.append(f"visual custody receipt dimensions do not match for {path_text}")
        if item.get("bytes") != path.stat().st_size:
            errors.append(f"visual custody receipt byte count does not match for {path_text}")
        if item.get("sha256") != hashlib.sha256(path.read_bytes()).hexdigest():
            errors.append(f"visual custody receipt digest does not match for {path_text}")

    manual_review = receipt.get("manual_visual_review", {})
    if manual_review.get("status") != "passed":
        errors.append("visual custody receipt lacks a passed manual visual review")


def check_documentation_custody(repo: Path, errors: list[str]) -> None:
    authorship_path = repo / "verification/documentation/documentation-authorship.json"
    review_path = repo / "verification/documentation/documentation-review.json"
    try:
        authorship = json.loads(read_text(authorship_path, errors))
        review = json.loads(read_text(review_path, errors))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"invalid documentation custody receipt: {exc}")
        return

    records: list[str] = []
    authored_files = authorship.get("authored_files", [])
    if not isinstance(authored_files, list) or len(authored_files) != 17:
        errors.append("documentation authorship receipt must bind exactly 17 customer files")
        return
    for item in authored_files:
        if not isinstance(item, dict) or not item.get("path"):
            errors.append("documentation authorship receipt contains an invalid file record")
            continue
        path_text = str(item["path"])
        path = repo / path_text
        if not path.is_file():
            errors.append(f"documentation authorship file is missing: {path_text}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if item.get("bytes") != path.stat().st_size:
            errors.append(f"documentation authorship byte count does not match: {path_text}")
        if item.get("sha256") != digest:
            errors.append(f"documentation authorship digest does not match: {path_text}")
        records.append(f"{path_text}\0{digest}")

    fingerprint = hashlib.sha256("\n".join(records).encode("utf-8")).hexdigest()
    if authorship.get("documentation_fingerprint") != fingerprint:
        errors.append("documentation authorship collection fingerprint does not match")
    if review.get("documentation_fingerprint") != fingerprint:
        errors.append("documentation review fingerprint does not match authorship")

    bound_objects = [
        authorship.get("documentation_manifest", {}),
        authorship.get("evidence_packet", {}),
        authorship.get("authoring_response", {}),
        *authorship.get("execution_evidence", []),
    ]
    for item in bound_objects:
        if not isinstance(item, dict) or not item.get("path"):
            errors.append("documentation authorship receipt contains an invalid evidence record")
            continue
        path_text = str(item["path"])
        path = repo / path_text
        if not path.is_file():
            errors.append(f"documentation authorship evidence is missing: {path_text}")
            continue
        if item.get("bytes") != path.stat().st_size:
            errors.append(f"documentation authorship evidence byte count does not match: {path_text}")
        if item.get("sha256") != hashlib.sha256(path.read_bytes()).hexdigest():
            errors.append(f"documentation authorship evidence digest does not match: {path_text}")


def check_identity_and_private_paths(repo: Path, errors: list[str]) -> None:
    public_files = [repo / "README.md", *(repo / path for path in PAGE_FILES)]
    private_patterns = [
        re.compile(r"[A-Za-z]:\\"),
        re.compile(r"\bfile://", re.I),
        re.compile(r"\blocalhost\b", re.I),
        re.compile(r"\b127\.0\.0\.1\b"),
    ]
    for path in public_files:
        if not path.is_file():
            continue
        text = read_text(path, errors)
        for pattern in private_patterns:
            if pattern.search(text):
                errors.append(f"private or local path marker in {relative(path, repo)}")

    visual_names = [path.name.lower() for path in (repo / "docs/assets/images").glob("*")]
    forbidden_name_parts = ["headshot", "portrait", "likeness", "impact-theory"]
    for name in visual_names:
        if any(part in name for part in forbidden_name_parts):
            errors.append(f"forbidden identity-coded visual filename: {name}")


def check_readme(repo: Path, errors: list[str]) -> None:
    readme = read_text(repo / "README.md", errors)
    required = [
        "docs/assets/images/impactful-tom-header.png",
        EXPECTED_ROOT,
        "https://github.com/Stunspot/impactful-tom/releases/tag/v1.0.0",
    ]
    for marker in required:
        if marker not in readme:
            errors.append(f"README missing public presentation marker: {marker}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()

    repo = args.repo.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    check_required_files(repo, errors)
    check_config(repo, errors)
    permalink_map = check_pages(repo, errors)
    check_layout_and_css(repo, errors)
    check_links(repo, permalink_map, errors)
    check_metadata(repo, errors)
    check_public_claims(repo, errors)
    check_accessibility_content(repo, errors)
    check_pngs(repo, errors)
    check_visual_custody(repo, errors)
    check_documentation_custody(repo, errors)
    check_identity_and_private_paths(repo, errors)
    check_readme(repo, errors)

    return emit("documentation_site", errors, warnings)


if __name__ == "__main__":
    raise SystemExit(main())
