# Metered verification preflight

## Capacity

GitHub Actions private-repository capacity is unavailable by the operator's 2026-08-12 account observation; remaining minutes are not readable here, refresh is expected 2026-09-01, and paid overage is not authorized.

## Expansion

2 triggers Ã— 1 matrix job Ã— 1 attempt Ã— unspecified ceiling minutes Ã— unknown provider multiplier = unknown estimated billed minutes. Raw runner-minute total is unknown because the workflow declares no ceiling and no current provider multiplier was retrieved.

## Decision

HOLD_PROVIDER_UNAVAILABLE. No GitHub-hosted workflow was dispatched.

## Substitute

The repository's local unittest suite, four static gates, and the exact pinned TestForge line-ending action bytes were executed locally. This substitute does not prove: GitHub's runner/image behavior, push and pull-request trigger behavior, permission or secret handling, artifact handling, or status integration.

## Authority

No paid execution is requested or authorized. Publication must retain `[skip ci]` and satisfy the protected status context only from the exact local verifier evidence if the ruleset permits an explicit commit status.
