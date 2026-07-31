# TestForge Pages correction review — initial

Verdict: `REVIEW_FAIL`

Reviewer: Fresh-context TestForge verification reviewer 1.1.2
Target: `post-release-pages-and-visuals` working tree based on `913161c29d09e1b587e7e2c5522ef3ba0ca94dfe`
Environment: Windows local repository
Evidence cutoff: 2026-07-30

## F-001 — future-false release lineage

Severity: high

`README.md` and `docs/provenance-and-verification.md` said public `main` and the immutable `v1.0.0` tag resolve to the same release commit. Publishing the correction necessarily advances `main` while the tag remains sealed.

Required repair: state the tag’s immutable release lineage and make `main` a moving post-release documentation branch.

Disposition: resolved in the working tree. The public wording and `PV-O-005` now preserve the temporal boundary.

## F-002 — non-discriminating host-claim oracle

Severity: high

The original claim checker required aggregate host-state keywords but would also pass a sentence asserting that clean installation, restart resilience, causal invocation, and Claude behavior were verified.

Required repair: require explicit unobserved semantics on canonical claim surfaces and add negative fixtures for each dangerous positive claim.

Disposition: resolved in the working tree. The validator now checks canonical negative semantics and rejects positive claims for all four host-state classes; the four hostile fixtures pass by being rejected.

## F-003 — candidate custody not yet bound

Severity: medium

Before a candidate commit exists, `HEAD` still identifies the release commit and ordinary `git diff` omits untracked correction files. The evidence cannot yet bind the complete candidate or demonstrate the final diff scope.

Required repair: create the complete local candidate commit, enumerate its exact diff against the release commit, rerun the validators against that revision, and bind the review to the resulting commit.

Disposition: open until the candidate commit and follow-up review exist.

## Boundary

Corrected live Pages routes and assets, the repository social-preview setting, clean public-route installation, restart resilience, causal host invocation, and Claude live behavior remain later evidence conditions rather than additional source defects.
