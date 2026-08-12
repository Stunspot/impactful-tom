# TestForge cycle 4 independent review

- Verdict: `REVIEW_FAIL`
- Candidate commit: `455d7f7497435070d51e78e6e5c4895267f3bf94`
- Candidate tree: `06eb5aca9dcd0432eea7ceef42e70bd37a0e4edf`
- Base: `40cbbdd98f60eeda7b9635918f82f9557b1db739`
- Package cutoff: `2026-08-12T18:41:27.6030968Z`
- Reviewer cutoff: `2026-08-12T18:44:19.1520309Z`
- Reviewed manifest SHA-256: `e6b20e33865d8288fe3569d8cc79523628a7d886f6fdecc12b89bb8c57ccb046`

## High finding: dated exception did not bind the old object

The lineage oracle treated a date as enough to qualify a positive live-visual clause as old evidence whenever another clause in the same Markdown item supplied a historical label and replacement disclaimer. It did not reject a dated clause that expressly named this remediation's replacement bytes.

Discriminating counterexample:

> On 2026-08-11, public readback confirmed this remediation's replacement social card is live. It is historical evidence and does not establish that this remediation's replacement social card is live.

Observed classification: `positive=True`, `dated_old_exception=True`, `flagged=False`.

Required repair: make an old-evidence exception clause-local and ineligible for current, remediation, replacement, redesigned, latest, or equivalent present bytes. Add dated replacement regressions using period and semicolon forms in every governed historical surface.

## Consequence

`R-LINEAGE` is unresolved. Candidate four is withdrawn and `NOT_READY`. The unchanged governed documentation and presentation receipts remain bound; the verifier and its tests require a fresh TestForge cycle.