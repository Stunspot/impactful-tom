# Troubleshooting and recovery

## The plugin or skill does not appear

For Codex, first run:

```powershell
codex plugin marketplace list
codex plugin list --marketplace impactful-tom --json
```

If the marketplace or plugin is absent, confirm that `https://github.com/Stunspot/impactful-tom` and the named release are publicly readable. Record the command output and exact error before re-adding the marketplace or plugin. Do not treat repeated installation attempts as proof that the source is available.

For Claude Code or a generic host, confirm that the complete `impactful-tom` folder—not just `SKILL.md`—was placed in the skill location required by that host version. If the host has no documented directory-skill route, stop rather than making a partial copy.

## The skill appears but the response is generic

Start a new session, then provide one live decision with an outcome, relevant facts, and the decision you need to make. A vague request for motivation gives the method less to work with than a decision such as "Should we continue this channel test after four weeks with no qualified leads?"

If the response is still generic, ask it to name the decision, constraint, evidence posture, owner, threshold, review horizon, and interpretation. If it invents facts or treats an inference as certain, correct that specific error and ask for the move to be revised.

## The response turns into a macro lecture

Ask for the causal path from the macro condition to your runway, price, demand, input cost, hiring, capital, regulation, or counterparty risk. If it cannot name one, ask it to leave macro out and return to the operating constraint.

## The response suggests an unsafe shortcut

Do not execute it. Preserve the prompt and response, identify the high-consequence area, and seek current authoritative or qualified review. Impactful Tom is not a legal, tax, investment, medical, regulatory, safety, or security authority.

## A Founder Case was not saved or needs correction

Confirm whether you explicitly requested a file and chose the location. If not, treat the conversation as session-only. If you did choose a location, ask the host to read back the exact file before assuming it was written. Correct an inference visibly. For deletion, authorize the exact target and confirm the host's observed result.

## You need to stop safely

You can stop using the skill without changing your business state. Save the current decision, the evidence you already have, and the next review condition somewhere you control. Resume when you can supply the missing fact, obtain qualified review, or run the bounded move.

## What to include in a support report

Include the host and version, whether the marketplace and plugin were listed, the exact installation or activation error, the prompt you used with sensitive details removed, the unexpected result, and the steps already tried. Do not include credentials or private source material.

Use [Impactful Tom support](../SUPPORT.md) for ordinary issues. Use the private route in [Security policy](../SECURITY.md) for vulnerabilities or sensitive reports.
