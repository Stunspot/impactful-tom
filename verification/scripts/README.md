# Static verification commands

These dependency-free checks establish package structure and content-boundary evidence. They do not execute a model or establish clean-host installation.

Run from the repository root:

```powershell
python -X utf8 verification/scripts/check_content_boundaries.py
python -X utf8 verification/scripts/check_release_exclusions.py
python -X utf8 verification/scripts/check_distribution_topology.py --claude-root dist/claude-code/impactful-tom --require-claude
```

`check_release_exclusions.py` reads `verification/source-custody.json` and scans only publishable surfaces by default (`.agents`, `plugins`, `README.md`, `docs`, `dist`, and `release`). It deliberately excludes internal development and verification records from its candidate scope.
