# Impactful Tom Security Policy

## Report a vulnerability privately

Do not disclose a suspected vulnerability, credential, private business record, personal information, or exploit detail in a public issue.

After the repository is public, use GitHub's private vulnerability-reporting route:

https://github.com/Stunspot/impactful-tom/security/advisories/new

If that route is unavailable, contact Collaborative Dynamics through https://collaborative-dynamics.com and identify the message as an Impactful Tom security report. Include the affected version, host, reproduction conditions, impact, and a safe way to validate the report. Do not include real secrets or unnecessary customer data.

## Supported release

Security corrections are assessed against the latest public release. Older versions may be asked to reproduce on the latest release before a fix is evaluated.

## Package boundary

Impactful Tom 1.0.0 contains no hosted service, account, connector, MCP server, hook, telemetry, analytics, or automatic network request. The AI host, model provider, operating system, repository host, and user-selected tools remain separate security boundaries with their own policies and update duties.
