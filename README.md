# Rootly agent skills

Rootly's plugin for AI coding agents: Claude Code, Codex, Cursor, and Devin.
It connects your agent to your Rootly account and teaches it how to work an
incident, so you can ask "what is going on with checkout right now?", "is it
safe to deploy this?", or "who is on call for payments?" and get answers
grounded in your real incidents, alerts, services, and schedules.

## What's inside

- **Seven skills.** Each is a `SKILL.md` workflow with its own reference
  material: which Rootly records to pull, how to weigh evidence, what the
  answer should look like, and a worked example. They cover incident response,
  alert triage, deploy checks, service health, on-call, incident
  communications, and retrospectives.
- **Rootly MCP connection.** The plugin bundles Rootly's hosted MCP server, so
  after a one-time OAuth sign-in your agent reads live incidents, alerts,
  services, schedules, and retrospectives. No API keys to manage.
- **Slash commands.** Short aliases such as `/rootly:respond`,
  `/rootly:oncall`, and `/rootly:retro` route to the right skill in Claude Code
  and Cursor.
- **Read-only guardrails.** Allowlists of Rootly's read-only tools for Claude
  Code and Codex, so an agent in a shared session cannot page, edit, or publish.

## How it helps

- **During an incident:** impact, recent changes, related incidents, and
  mitigation options with the evidence behind each, plus who to pull in.
- **Before a deploy:** GO / CAUTION / NO-GO from incident history, service
  health, and current on-call coverage.
- **On call:** coverage lookups, complete shift handoffs, and swap options.
- **Afterwards:** stakeholder updates drafted for the right audience, and
  retrospective evidence with facilitation questions.

## Skills

| Skill | What it does |
|---|---|
| [Incident response](skills/incident-response/SKILL.md) | Investigate impact and recent changes; recommend mitigation and responders |
| [Alert triage](skills/alert-triage/SKILL.md) | Recommend a new incident, attachment, wait, or dismissal — with evidence |
| [Deploy check](skills/deploy-check/SKILL.md) | GO / CAUTION / NO-GO with reasons; staffing warnings kept separate |
| [Service health](skills/service-health/SKILL.md) | Errors, latency, and traffic against baselines, plus ownership context |
| [On-call](skills/on-call/SKILL.md) | Coverage lookups, complete shift handoffs, provisional swaps |
| [Incident comms](skills/incident-communications/SKILL.md) | Audience-specific drafts — no invented impact or recovery estimates |
| [Retrospective](skills/retrospective/SKILL.md) | Evidence and facilitation questions; humans own the conclusions |

## Install

Each client installs one plugin named `rootly` that bundles the seven skills,
slash-command aliases, and the Rootly MCP server. Pick your client:

**Claude Code**

```sh
claude plugin marketplace add Rootly-AI-Labs/agent-skills
claude plugin install rootly@rootly-agent-skills --scope local
```

**Codex**

```sh
codex plugin marketplace add Rootly-AI-Labs/agent-skills
codex plugin add rootly@rootly-agent-skills
```

**Cursor**

Install **Rootly** from the Cursor Marketplace. Cursor reads the repository's
`plugin.json` directly, so a local checkout loads the same way.

**Devin** (CLI, Desktop, and cloud sessions)

```sh
devin plugins install Rootly-AI-Labs/agent-skills
```

**Skills only, any agent**

```sh
npx skills add Rootly-AI-Labs/agent-skills
```

This installs the skills as plain `SKILL.md` files without the bundled MCP
server or aliases; connect Rootly MCP through your client yourself.

Then invoke a skill, for example `/rootly:incident-response` in Claude Code
and Devin or `$rootly:incident-response` in Codex. The first call prompts for
Rootly sign-in through the client's MCP flow; never paste a token into chat.
Local checkouts, read-only restrictions, and per-client quirks are in
[installation](docs/install.md).

## Read-only by design

The skills recommend and draft only — they never page responders, modify
incidents, change schedules, publish messages, or act on production. Prompt
instructions are not access controls: apply the client restrictions in
`adapters/` before using live data. See [safety](docs/safety.md) and
[migration](docs/migration.md).

## Status

`1.0` — first release of this package, which replaces the earlier Rootly
plugins for Claude Code and Cursor. Read-only by design: the earlier plugins'
write actions are not included yet; see [migration](docs/migration.md).

## License

Apache-2.0. Copyright 2026 Rootly, Inc. See [LICENSE](LICENSE) and
[NOTICE](NOTICE).
