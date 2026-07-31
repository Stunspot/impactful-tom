---
layout: default
title: Install, update, and uninstall
description: Install Impactful Tom for Codex or a generic skill host, verify the result, update safely, and remove it cleanly.
permalink: /install/
eyebrow: Host setup
---

## Current release status

These instructions target the public version `1.1.0` release. Its tag, release, five assets, checksum ledger, Pages documentation, and repository social preview passed direct public readback on July 31, 2026. Exact-version host installation has not yet been observed.

Before installing, open the [version 1.1.0 release page](https://github.com/Stunspot/impactful-tom/releases/tag/v1.1.0) and confirm that the tag, release archives, and checksum ledger are still publicly readable. If the page is absent or the checksums do not match, stop; `main` is not an immutable-release substitute.

The [evidence page]({{ '/evidence/' | relative_url }}) separates static package checks from public readback and live-host evidence. A visible release archive does not, by itself, establish installation, discovery, invocation, or first success.

The exact final package has not been installed through a clean public route. Restart resilience and causal host invocation remain unobserved.

## Codex repository-marketplace route

### Before you begin

You need a supported Codex environment with plugin access and network access to the public repository. The marketplace source is `Stunspot/impactful-tom`, pinned to `main`. If the source does not resolve, record the exact command and error before retrying; do not improvise a partial installation from copied files.

### Add the marketplace and install the plugin

Add the public marketplace and install the plugin:

```powershell
codex plugin marketplace add Stunspot/impactful-tom --ref main
codex plugin add impactful-tom@impactful-tom
```

Then start a new Codex session before asking for a founder decision. You can inspect what Codex sees with:

```powershell
codex plugin marketplace list
codex plugin list --marketplace impactful-tom --json
```

An installation command returning a result is not, by itself, proof that the skill was selected or behaved well. Use a simple live decision such as the prompt in [Getting started]({{ '/getting-started/' | relative_url }}), then confirm that the response is relevant to the decision you gave it.

### Update the marketplace source

When a later published release tells you to update, refresh the configured marketplace and inspect the result:

```powershell
codex plugin marketplace upgrade impactful-tom
codex plugin list --marketplace impactful-tom --json
```

If the listed installed version is not the version you intend to use, remove and add the plugin again:

```powershell
codex plugin remove impactful-tom@impactful-tom
codex plugin add impactful-tom@impactful-tom
```

Start a new session after an install, re-install, or update. Keep the command output if a release maintainer asks for troubleshooting evidence.

### Uninstall from Codex

Remove the installed plugin:

```powershell
codex plugin remove impactful-tom@impactful-tom
```

If you no longer want Codex to track the marketplace itself, remove that separately:

```powershell
codex plugin marketplace remove impactful-tom
```

Removing a plugin and removing a marketplace are different actions. The first removes the installed plugin; the second removes the configured source.

## Claude Code

The release includes one self-contained directory: `dist/claude-code/impactful-tom`. The Claude Code/generic skill directory passes structural checks without live-host evidence. A live Claude Code installation, discovery, invocation, and first-success test have not been observed.

Claude Code's [official skill documentation](https://code.claude.com/docs/en/slash-commands) defines two local installation scopes:

- **Personal:** place the complete folder at `~/.claude/skills/impactful-tom/`. The entry point must be `~/.claude/skills/impactful-tom/SKILL.md`. Use this when you want the skill available across your projects.
- **Project:** from the project root, place the complete folder at `.claude/skills/impactful-tom/`. The entry point must be `.claude/skills/impactful-tom/SKILL.md`. Use this when the skill should apply only to that project.

Choose one scope unless you intentionally manage both. A personal skill with the same name takes precedence over a project skill.

### Install and check the directory

1. Expand the Claude Code/generic distribution. It should contain one top-level `impactful-tom` folder.
2. Copy that complete folder to `~/.claude/skills/impactful-tom/` for personal use or `.claude/skills/impactful-tom/` for project use. Preserve every supplied file and subdirectory; do not copy only `SKILL.md`.
3. Confirm that the installed shape has no extra nesting:

   ```text
   impactful-tom/
   ├── SKILL.md
   ├── package-manifest.yaml
   ├── ATTRIBUTION.md
   ├── LICENSE.md
   ├── NOTICE.md
   ├── TRADEMARKS.md
   ├── assets/
   ├── evals/
   └── references/
   ```

   If the entry point is instead at `impactful-tom/impactful-tom/SKILL.md`, move the inner folder up one level.
4. If `~/.claude/skills/` or the project's `.claude/skills/` already existed when the current Claude Code session started, Claude Code watches it and should detect the new skill without a restart. If you created that top-level skills directory during the session, restart Claude Code so it can watch the directory.

### Invoke it and confirm first value

In Claude Code, invoke the directory name directly with one observable founder decision:

```text
/impactful-tom We ship features every week, but retention is flat. Find the constraint and give us one move with an owner, threshold, and review point.
```

A first-success response stays on that decision, distinguishes evidence from inference, names a plausible constraint, and proposes a bounded move with an owner and review condition. That response is a functional check in your host; it is not evidence of universal reliability or professional advice.

If `/impactful-tom` is not available, recheck the entry-point path and extra-nesting condition first. If the top-level skills directory did not exist when the session started, restart Claude Code, then try `/impactful-tom` again. Do not change the package contents until those path and restart checks are complete.

### Update

1. Save any user-created `founder-case.md` outside the installed skill directory. The package does not own or migrate that file.
2. Replace the entire installed `impactful-tom` folder with the complete replacement folder at the same personal or project path. Do not merge selected files from different versions.
3. Recheck the directory shape and run the first-value invocation again.

Claude Code watches changes inside an existing skills directory during the current session. Start a new conversation for the update check so a previously loaded skill body is not mistaken for the replacement version. Restart Claude Code only if the top-level skills directory did not exist when the session started.

### Uninstall

1. Save any Founder Case you want to keep outside the skill directory.
2. Remove only the installed `~/.claude/skills/impactful-tom/` or `.claude/skills/impactful-tom/` folder, matching the scope you chose.
3. Start a new conversation and confirm that `/impactful-tom` is no longer available.

Removing the skill does not delete a Founder Case stored elsewhere. Claude Code watches removals from an existing skills directory; use the same restart boundary if the top-level directory was created after the session began.

## Other generic skill hosts

Skill locations and activation flows vary outside Claude Code. Use the host's current official skill-installation instructions and install the complete `impactful-tom` directory, preserving `SKILL.md`, `assets`, `evals`, `references`, the package manifest, and the included legal files.

If the host cannot install a self-contained skill directory, stop rather than improvising a partial copy. Record the host and version, the installation location you tried, and the exact error. That is the re-entry evidence needed for a compatible distribution.

## A safe first check after any install

1. Start a new conversation or session.
2. Give one live founder decision and enough context to make a route possible.
3. Check that the response stays on the decision, names a plausible constraint, separates evidence from inference, and proposes a bounded next move.
4. Do not treat this check as legal, financial, tax, or other professional advice.

If the skill does not appear or does not use its method, go to [Troubleshooting and recovery]({{ '/troubleshooting/' | relative_url }}).
