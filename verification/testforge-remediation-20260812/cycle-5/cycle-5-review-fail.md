# TestForge cycle 5 independent review

- Verdict: `REVIEW_FAIL`
- Candidate commit: `be999dfe076c3a8c83eeb733b2238b2909245b3f`
- Candidate tree: `cc88e68822e37f5266cb63111b5ccd0528eaf94b`
- Base: `40cbbdd98f60eeda7b9635918f82f9557b1db739`
- Package cutoff: `2026-08-12T18:56:19.8359113Z`
- Reviewer cutoff: `2026-08-12T19:04:10.6309945Z`
- Reviewed manifest SHA-256: `4e5349a19aefdbcd316ddd0d132d1182bf4c7cd62e49115a117e349773eba8a5`

## High finding: historical-clause laundering remained

The new present-byte exclusion constrained only one historical exception. A broader `sentence_historical` allowance and the disclaimer allowance could still pardon a positive current/replacement/remediation/redesigned/latest/new/updated/refreshed visual-publication claim by borrowing a denial elsewhere in the same Markdown item. Fully re-bound README, changelog, and provenance probes passed the complete documentation gate. Neighboring bullets were isolated correctly; same-item periods and semicolons remained exploitable.

Required repair: eliminate cross-clause historical and disclaimer borrowing. A pending or negative boundary must precede the visual-publication claim within the same clause. Add fully re-bound regressions for the reported terms and semantic equivalents across periods, semicolons, wrapped lines, same-item contradictions, and neighboring bullets.

## Medium finding: EOL execution evidence was empty

`EXEC-EOL` claimed PASS, but `raw-line-ending-policy.txt` was zero bytes and `T-EOL.path` referenced older evidence. Git emitted the pinned verifier to the console while the temporary file remained empty; Python then exited successfully after running no code.

Required repair: materialize the exact pinned verifier blob byte-for-byte, prove its blob identity, retain substantive JSON output, and bind both `T-EOL` and `EXEC-EOL` to the same cycle-specific receipt.

## Consequence

Candidate five is withdrawn and `NOT_READY`. Its ordinary 12-test suite and four static gates passed, but they do not overcome the proven lineage-oracle and EOL-evidence defects.