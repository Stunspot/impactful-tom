# Hesperos Pages and visual-documentation authoring evidence

Run ID: `HESPEROS-IMPACTFUL-TOM-20260730-PAGES-01`

## Authorized correction

Sam clarified that complete public Augment documentation includes the GitHub Pages setup and a coherent visual family, including a README header and social card. This run corrects that omitted public-documentation surface without redesigning Impactful Tom or changing the immutable `v1.0.0` tag and release assets.

## Reader and task model

The primary reader is a pre-founder, validating founder, stalled founder, or functional operator trying to make one consequential business decision. The public journey is:

1. Understand the product promise and independent, unofficial status.
2. Decide whether the method fits the live decision.
3. Install through the appropriate host route.
4. Reach first value with one bounded prompt.
5. Inspect privacy, authority, macro, provenance, and verification boundaries.
6. Recover, update, uninstall, or seek support.

## Information architecture

The Pages navigation is deliberately small: Home, Start, Install, Boundaries, Evidence, and GitHub. The footer carries the release, support, privacy, and license routes. Troubleshooting remains linked from the relevant installation and recovery moments rather than competing in the primary navigation.

The site uses the existing `main:/docs` Pages source, project base path `/impactful-tom`, one dependency-free Jekyll layout, one stylesheet, and baseurl-safe Liquid links. Root policy files remain canonical and are linked through intentional absolute GitHub URLs rather than duplicated under `docs/`.

## Visual system and custody

The existing name-free founder-constraint mark is the sole identity anchor. The README header, social card, web-app marks, touch icon, and favicons are deterministic derivatives generated from that source through `development/build_documentation_visuals.ps1`. No headshot, likeness, quotation, signature, cloned voice cue, or third-party logo is used.

The Imagegen skill’s own guidance favored using the established mark rather than generating a competing logo. The resulting visual family uses the mark’s deep navy, cyan, and gold palette and original system-font typography. Exact source, generator, output dimensions, byte counts, hashes, and manual raster observations are retained in `verification/documentation/visual-assets-custody.json`.

## Accessibility decisions

- A skip link precedes the header and targets the single main landmark.
- Primary navigation has a programmatic label.
- Every page has one visible page-level heading, supplied by content or the layout.
- Decorative mark images use empty alternative text and `aria-hidden="true"`.
- Focus uses a two-color ring rather than color alone.
- Layout reflows at narrow widths and honors reduced-motion preferences.
- Links describe their destination or task.
- The README header has meaningful alternative text.
- No accessibility-conformance claim is made.

## Evidence and claim control

Observed before publication of this correction:

- the repository, annotated `v1.0.0` tag, release, and five release assets are public;
- GitHub Pages is configured from `main:/docs`, reports built, and enforces HTTPS;
- the corrected source passes the dependency-free Pages validator;
- all 16 public Markdown documents pass the Hesperos accessibility lint;
- the documentation project schema is valid;
- content-boundary, release-exclusion, and dual-host topology checks pass; and
- the four representative visual assets were manually inspected.

Still unearned at this stage:

- the corrected live Pages routes, metadata, stylesheet, and images;
- the repository-level social-preview setting;
- clean installation and first success through the public route;
- restart resilience or causal host invocation; and
- live Claude Code installation, discovery, invocation, or first value.

## Authoring disposition

The customer documentation correction is constructed and locally verified. It is ready for fresh-context accessibility and TestForge review, not yet ready for a live Pages claim.
