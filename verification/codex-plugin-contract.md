# Codex plugin contract check

Observed on 2026-08-11 for Impactful Tom 1.1.1.

## Current official product boundary

OpenAI's current [Plugins in Codex](https://help.openai.com/en/articles/20001256/) documentation says plugins may contain skills, apps, and app templates. Skill-only plugins remain usable without an app dependency when plugin and skill access are available, subject to plan, rollout, workspace, and role controls. Impactful Tom is a skill-only plugin: it declares no app, app template, MCP server, authentication flow, external-data dependency, or external action.

That official product documentation describes eligibility and administration. It does not prove that this public repository installs or that a host selected the skill.

## Current local CLI contract

The installed `codex-cli 0.144.5` help was read directly without changing configuration. It reports:

- `codex plugin marketplace add <SOURCE>` accepts `owner/repo` and `--ref <REF>`;
- `codex plugin add <PLUGIN@MARKETPLACE>` installs from a configured marketplace snapshot;
- `codex plugin marketplace upgrade [MARKETPLACE_NAME]` refreshes a configured Git marketplace;
- `codex plugin remove <PLUGIN@MARKETPLACE>` removes the installed plugin; and
- `codex plugin marketplace remove <MARKETPLACE_NAME>` removes the configured source separately.

This confirms the documented command contract:

```powershell
codex plugin marketplace add Stunspot/impactful-tom --ref main
codex plugin add impactful-tom@impactful-tom
```

The help readback is command-surface evidence only. It does not establish clean public-route installation, discovery, invocation, restart resilience, or first success for Impactful Tom 1.1.1.