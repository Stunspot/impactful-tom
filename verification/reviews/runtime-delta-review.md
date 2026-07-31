# Independent TestForge runtime-delta review

## Verdict

`PASS_WITH_CONDITIONS`

The prior sealed `f03260ecb4024a964f213fe115874e3935d16a503c06675d1fa8dd0e73734cc2` run truthfully supports the final package's founder method as inherited evidence. It is not represented as execution of the new whole package.

The reviewer independently reverified the old seal: 270 files and 550,968 bytes, with zero missing, changed, or extra artifacts. Its bounded result remains `PARTIAL`: 24 of 24 episodes valid, 20 demonstrated, four accepted partials, and zero failures.

## Delta evidence

The preserved prior cache contains 11 files. Against the current Codex skill root:

- nine shared files are byte-identical;
- only the `SKILL.md` frontmatter description and `agents/openai.yaml` routing description changed;
- the `SKILL.md` instruction body independently matches at SHA-256 `a17c7ac78926729f32baeb31f6f111beb6b175abac7748a2e9dc227c1d5df9e8`;
- evals, references, templates, and package manifest are byte-identical; and
- four legal and notice files were added.

The current Codex and Claude roots share 14 byte-identical files. Codex alone carries `agents/openai.yaml`. Both current roots passed the Augment validators with zero findings.

## Verification disposition

A full behavioral rerun is not required. Targeted founder-method cases are also not required because they would retest unchanged instructions while bypassing the changed routing surface.

The minimum additional evidence is a final public-route installed-host proof on the exact released bytes:

1. public installation receipt;
2. fresh-task catalog presence under the new description;
3. implicit selection from a representative founder request; and
4. a first-success response judged against an existing decision-critical case.

Resource loading should be captured if the host exposes it. If the host does not expose immutable read or invocation events, the causal limitation must remain explicit.

## Claim boundary

`f03260ec…` supports the unchanged founder method. It does not prove the current `ff495fd2f627d0e8f371d2480ad2b8f7a3f0707958f8dce6c83853505704006c` whole-package fingerprint, new routing metadata, all-case demonstration, stochastic reliability, Claude live behavior, or public-route health.
