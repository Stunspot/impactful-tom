# Install, update, and uninstall

## Current release status

Version `1.0.0` is prepared for publication at `Stunspot/impactful-tom`. At the current evidence cutoff, no public repository, GitHub release, release-asset readback, or public-route installation receipt exists. The commands in “Add the marketplace and install the plugin” are the intended release route and become a public availability claim only after those objects are observed.

The local Codex repository marketplace was configured on the current workstation, and an earlier candidate was installed and enabled with exact parity across its 11 model-facing runtime files at that evidence cutoff. A later fresh task catalog surfaced that installed skill and returned a representative founder response. The current release keeps the instruction body byte-identical, leaves nine other shared files unchanged, replaces the two catalog descriptions, and adds four legal and notice files. It therefore still requires installation and first-success readback through the final public route. The Claude Code/generic skill directory remains structurally checked without live-host evidence.

## Codex repository-marketplace route

### Before you begin

You need a supported Codex environment with plugin access and a published repository containing the marketplace. The marketplace source is `Stunspot/impactful-tom`, pinned to `main`. If the repository or release is not publicly readable yet, stop and use the evidence in “Current release status” rather than retrying alternate sources.

### Add the marketplace and install the plugin

When the repository is publicly readable, run:

```powershell
codex plugin marketplace add Stunspot/impactful-tom --ref main
codex plugin add impactful-tom@impactful-tom
```

Then start a new Codex session before asking for a founder decision. You can inspect what Codex sees with:

```powershell
codex plugin marketplace list
codex plugin list --marketplace impactful-tom --json
```

An installation command returning a result is not, by itself, proof that the skill was selected or behaved well. Use a simple live decision such as the prompt in [Getting started](getting-started.md), then confirm that the response is relevant to the decision you gave it.

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

## Claude Code and other generic skill hosts

The release includes one self-contained directory: `dist/claude-code/impactful-tom`. It has been structurally checked as a portable skill root. A live Claude Code installation, discovery, invocation, and first-success test have not been observed.

Because the documented skill location and activation flow can vary by Claude Code or generic host version, use that host's current official skill-installation instructions. Install the complete `impactful-tom` directory, preserving its internal `SKILL.md`, `assets`, `evals`, and `references` folders. Do not copy only `SKILL.md`; its relative resources are part of the package.

For an update, replace the entire installed `impactful-tom` directory with the replacement directory after saving any user-created Founder Case somewhere else. For removal, remove that installed directory using the host's documented uninstall or skill-management route. Removing the skill does not delete a Founder Case stored in a separate location you chose.

If your host cannot install a self-contained skill directory, stop there rather than improvising a partial copy. Record the host and version, the installation location you tried, and the exact error. That is the re-entry evidence needed for a compatible distribution.

## A safe first check after any install

1. Start a new conversation or session.
2. Give one live founder decision and enough context to make a route possible.
3. Check that the response stays on the decision, names a plausible constraint, separates evidence from inference, and proposes a bounded next move.
4. Do not treat this check as legal, financial, tax, or other professional advice.

If the skill does not appear or does not use its method, go to [Troubleshooting and recovery](troubleshooting.md).
