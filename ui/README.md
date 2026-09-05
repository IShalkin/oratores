# Run panel

A local page that watches a run directory and renders what the agents put there.

```
python ui/server.py            # http://127.0.0.1:8787
python ui/server.py --port 9000 --root /path/to/oratores
```

Stdlib only. If `jsonschema` happens to be installed it validates what the agents wrote and shows the failures at the top of the page; if not, it says so and renders anyway.

## What it is for

The package's central feature is offering options with the trade-off each source states. As terminal prose that is a paragraph people skim. As two cards side by side with the cost under each, it is a decision. The same is true of the objection map (seven fields per objection), the claim ledger (six claim types on one axis, five source statuses on the other) and the critic's findings.

The second thing it is for: a forked agent cannot ask you anything, because there is no return path — a question emitted mid-run ends the work instead of pausing it. So agents do not ask. They default, record what they assumed and why, and deliver. The **Assumptions** panel is where you find those and correct them.

## How it connects to the agents

It does not. There is no integration, no protocol, no SDK.

Agents write JSON files into `run/<id>/`. This server reads that directory. That is the whole interface, which is why it works the same under Claude Code, Codex or Copilot — anything that can write a file.

```
run/<id>/
  agents.json        the orchestrator: who ran, who is running, who was skipped
  brief.json         oratores-strategist
  evidence.json      oratores-evidence
  objections.json    oratores-adversary
  candidates.json    oratores-invention
  choices.json       any agent writes; the author decides
  assumptions.json   any agent writes; the author corrects
  findings.json      oratores-critic authors it; the orchestrator writes it
  artifact.md        the writer — the only agent that produces prose
```

The shapes are defined in [`../skills/oratores/schema/run-artifacts.schema.json`](../skills/oratores/schema/run-artifacts.schema.json) and explained for agents in [`references/run-artifacts.md`](../skills/oratores/references/run-artifacts.md) inside the skill.

Every file is optional. A run that skipped a specialist has no file for it and the panel renders an empty section, which is a real state and not an error.

## The rule that matters

**Nothing in the package depends on this running.** With the server off you still have the run directory and the artifact; the skill works headless and always must. An agent must never wait for the panel, poll it, or assume anyone is watching.

The panel writes back exactly two things, both only when you click:

- a decided choice, moved from `open` into `decided` in `choices.json`
- a corrected assumption, written into `assumptions.json`

Nothing else here writes to disk. It cannot edit the artifact, re-run an agent, or change a module.

## Deliberate limits

**No live prompting.** An agent cannot block on a browser click, so this version is observe-and-correct: you see what landed, fix a wrong assumption, and re-run the affected agent yourself. Making the orchestrator wait on a decision file is possible and adds a new way for a run to hang — the exact failure this design exists to avoid — so it is not here.

**No build step.** One HTML file, one stylesheet, one script, no `node_modules`. Live updates arrive over server-sent events, polling file modification times once a second.

**Localhost only.** It binds `127.0.0.1` by default and serves your working files. Do not expose it.
