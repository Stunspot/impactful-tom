# Codex plugin contract check

Observed on 2026-07-30.

## Current official product boundary

OpenAI's current [Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256-plugins-in-codex) documentation says that plugins may contain skills, apps, and app templates; skill-only plugins remain available without an app dependency, subject to plan, workspace, role, region, rollout, and supported-surface constraints. It also distinguishes plugin installation policy from app permissions and tells users to refresh a plugin imported from a marketplace when updating it.

Impactful Tom 1.0.0 is intentionally a skill-only plugin. It declares no app, app template, MCP server, external data dependency, or external action. The official page does not by itself prove that this repository can be imported or installed.

## Current local CLI contract

The installed `codex` CLI help was read directly on the named host. It reports:

- `codex plugin marketplace add <SOURCE>` accepts a local path, `owner/repo[@ref]`, HTTPS Git URL, or SSH Git URL.
- `--ref <REF>` pins the Git ref used when adding a marketplace.
- `codex plugin add <PLUGIN[@MARKETPLACE]>` installs a plugin from a configured marketplace snapshot.
- `codex plugin marketplace upgrade <MARKETPLACE>` refreshes a configured Git marketplace.
- plugin removal and marketplace removal are separate commands.

This supports the intended public route:

```powershell
codex plugin marketplace add Stunspot/impactful-tom --ref main
codex plugin add impactful-tom@impactful-tom
```

The route remains **documented but unverified** until the public repository exists and a clean target context independently observes marketplace addition, installation, discovery, invocation, and first-success behavior.
