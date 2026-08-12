# TestForge cycle 3 — REVIEW_FAIL

- Candidate: `a38bf7b5d78b3cef32f8b5cb1631677a5472db3b`
- Base: `40cbbdd98f60eeda7b9635918f82f9557b1db739`
- Tree: `c3267b5eca20d456cc88bca68fbdc738b3f362a8`
- Manifest SHA-256: `8e680b675ca02f41d07ac3f538b5c0ab54eba576c7376c73433627d3780b052f`
- Reviewer cutoff: `2026-08-12T18:34:04.7709997Z`

Verdict: `REVIEW_FAIL` / candidate `NOT_READY`.

High finding: blank-line paragraph splitting still flattened contiguous changelog bullets. A neighboring pending bullet could pardon the exact stale live claim, while the hostile fixtures only inserted blank-line prose.

Required revision: treat Markdown items independently, add the exact escaped sentence as a contiguous Unreleased bullet, and reject a contradictory positive sentence inside an otherwise historical item. Governed customer and presentation bytes were correct and therefore did not require another fingerprint or Hesperos/accessibility rerun.
