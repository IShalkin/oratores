# Run Artifacts — what to write, where, and in what shape

A run is one directory, `run/<run_id>/`, holding one job. Each specialist writes exactly one file into it; the writer reads all of them and produces `artifact.md`. No agent rewrites a file another agent owns.

Every file is optional. A skipped specialist leaves no file — a valid finished state, not a failure, rendered as an empty panel rather than an error. The shape is fixed by [../schema/run-artifacts.schema.json](../schema/run-artifacts.schema.json); follow this page and you need not open it.

## Who writes what

| Agent | File | Contents |
|---|---|---|
| `oratores` (orchestrator and writer) | `artifact.md`, `agents.json`, `findings.json` | The deliverable — the only prose in the run — plus the manifest, and the critic's findings transcribed verbatim |
| `oratores-strategist` | `brief.json` | Objective, segments, primary segment, resistance, ask |
| `oratores-evidence` | `evidence.json` | Labelled claims with locators, gaps, unusable material |
| `oratores-adversary` | `objections.json` | Charitable objections, where each is met, mechanism cost |
| `oratores-invention` | `candidates.json` | Unfiltered lines, metaphors, openings, titles |
| `oratores-critic` | — (`authored`: `findings.json`) | Produces the findings; holds no write tool, so the orchestrator writes the file. The manifest records both sides, so the transcription step has a named owner rather than being a step nobody performed |
| any agent | `choices.json` | Open decisions with priced options; decided ones |
| any agent | `assumptions.json` | What was defaulted, why, what moves if it is wrong |
| orchestrator | `agents.json` | Run manifest: id, task, mode, per-agent status |

## agents.json

The orchestrator's file, and no one else's. Required: `run_id`, `task`, `mode`, `agents`. `run_id` is the directory name, date-prefixed and readable. `task` is the request in one line as the user gave it, not a tidied paraphrase. `mode` is Explain, Design, Draft, Review or Rehearse; `form` records the rung reached on the form ladder. **The orchestrator stamps `finished` on each agent as it returns, not in one pass at the end.** It is the only writer of this file — `agents.json` carries neither the append discipline nor the id prefixes that make the two shared files survivable, so three parallel agents writing into it is the concurrency failure described below rather than a fix for anything. Stamping on return is a real clock reading at a real moment and it separates the stages; filling every field in one pass at the end produces a manifest where three parallel agents share a timestamp to the second and the writer's stage has zero duration, which cannot distinguish a completed stage from one that never ran. The reading is when the orchestrator observed the return, which is slightly later than the agent's own finish, and that is the honest limit of it. Each agent entry needs `name` and a `status` — pending, running, done, failed, skipped — and takes `writes`, `authored` (files whose content it produced but did not write — the critic's case), `started`, `finished`, and a one-line `note` for why it was skipped or what failed.

```json
{"run_id": "2026-09-05-board-q3", "mode": "Draft",
 "agents": [{"name": "oratores-evidence", "status": "skipped",
             "note": "no numbers in scope"}]}
```

## brief.json

Required: `objective`, `segments`, `primary_segment`, `ask`. In `objective`, `change` is the highest level the piece must actually reach — understand, believe, feel or do — and `specific_behaviour` states it concretely. `success_metric` may be null; null means stated as absent, never invented. Segments are behavioural, at least one, each with a `realistic_action`; record `intensity`, since an organized minority outweighs a passive majority. `ask.one_step` is required, and `whole_product` lists everything the after-state implies — an ask delivered at 80–90% is the standard failure. `heard_before` decides whether the opening can work at all. `urgency.state` is answered honestly: real, absent or manufactured. See [audience-and-intent.md](audience-and-intent.md).

```json
{"objective": {"audience": "regional GMs", "change": "do",
               "specific_behaviour": "name a pilot owner by Friday",
               "success_metric": null},
 "primary_segment": "pragmatic majority"}
```

## evidence.json

Required: `claims`. Each carries `id`, `text`, one `label` from the `LOG-04` type set — FACT, OBSERVATION, INTERPRETATION, FORECAST, HYPOTHESIS, ASPIRATION — where a later category never wears the clothes of an earlier one, and one `source_status` from the independent `LOG-04` source set — CHECKED, UNVERIFIED, CONTRADICTED, RECHECK, NOT_APPLICABLE — with its one-line `source_status_reason`, which the schema requires rather than invites.

Neither axis substitutes for the other: FACT with UNVERIFIED is a real state and the one worth catching before delivery, and softening the label to cover a source nobody could check is the defect the two fields exist to prevent. NOT_APPLICABLE is for the claim whose warrant is your own reasoning or intent — a projection has no source to check — and never for a fact nobody got round to checking, which is UNVERIFIED.

`locator` is required for anything presented as a quotation, and the schema refuses CHECKED without one; without a locator the claim's source status is UNVERIFIED and it is not attributed. `comparator_chosen_before_direction` may be null, and null means not recorded, which is itself a finding. `gaps` needs an `id` and `needed`, plus why it matters and who could supply it — other files cite gaps by id, so a gap without one has to be quoted, and the quote breaks on the first edit. `unusable` records what you rejected and why, with an id of its own.

```json
{"claims": [{"id": "C3", "text": "Churn fell 18% after the pilot",
             "label": "OBSERVATION", "source": "internal dashboard",
             "source_status": "UNVERIFIED",
             "source_status_reason": "no locator; the dashboard figure has not been checked",
             "comparator_chosen_before_direction": null}]}
```

## objections.json

Required: `objections`. Each needs `id`, `objection`, `charitable_reading` and `where`, and carries the rest of the `REF-01` set: `underlying_fear`, `response`, `limitation` and `next_action`. `limitation` is not optional in spirit — `REF-01` gates on every limitation appearing somewhere in the piece, so a response without one is claiming to be the whole truth. The charitable reading must be at least as strong as the one a real holder would make; a straw man here is a defect — `REF-01`, in [objection-and-refutation.md](objection-and-refutation.md). `is_it_correct` takes yes, partly or no, and `yes` is the cheapest information about the real obstacle. `where` is "in the piece", "in Q&A" or "passed over in silence" — answering everything signals fear, so silence is a decision and is recorded as one. `checked_first` lists, in order, the claim ids a hostile reader checks first. `mechanism_carrying` names the passage, the `MEC-01` mechanism doing the work, and its `stated_cost`; `dissent_position` records the `MEC-02` position taken and the one rejected, 1 to 5.

```json
{"objections": [{"id": "O1", "objection": "We tried this in 2023",
                 "charitable_reading": "2023 failed on staffing, not on the idea",
                 "is_it_correct": "partly", "where": "in the piece"}]}
```

## candidates.json

Deliberately unfiltered. Quantity is the point: the strong option usually appears after four or five have percolated up, and the first one is the cliche. Required: `sets`; each needs `for` (coined line, central metaphor, opening, argument, joke, title, story), `generator` — name the set from `INV-03` where you ran one of them, and describe the exercise in your own words where you did not — and `candidates`, each with an `id`, its `text`, and a `status` of open, kept or refused. `survives_paraphrase: false` is load-bearing — the effect lives in the wording, so do not translate it, do not touch it in revision, do not hand it to a speaker to reword. `kept` lists candidate ids, never candidate text, and `first_refused` records whether the first one was thrown away. Kill a candidate with `status: "refused"`, not with a note — a candidate killed in prose is one a later reader will use.

```json
{"sets": [{"for": "the coined line", "generator": "contrast-pairs",
           "candidates": [{"text": "We are not short of plans. We are short of Fridays.",
                           "survives_paraphrase": false}]}]}
```

## choices.json

Shared, and the point of the contract. Under `open`, each entry needs `id`, `question` and at least two `options`; add `procedure` and `raised_by`. An option needs `label`, `effect`, `cost` and `sourced`, and takes `condition` — when this option is the right one. `cost` and `sourced` are required precisely so that an unpriced trade-off cannot be produced by silence: write `"unpriced"` and `false` deliberately. `recommended` may be null. `decided` holds resolved entries: `id` and `chose` required, plus `rejected`, `by` (author, default or agent), `at` and `note`.

```json
{"open": [{"id": "CH2", "question": "Open on the failure or on the number?",
           "options": [{"label": "failure", "effect": "buys credibility early",
                        "cost": "unpriced", "sourced": false}],
           "conflict": {"between": ["oratores-strategist", "oratores-adversary"],
                        "about": "whether the room already knows"}}]}
```

## assumptions.json

Shared. Each entry under `assumptions` needs `id`, `input`, `assumed` and `because`, and should carry `changes_what` — what in the deliverable moves if this is wrong — and a `confidence` of safe, material or blocking. Leave `corrected_to` and `corrected_at` alone; the panel writes both, and no agent writes either. Under `blocking_gaps`, each entry needs an `id` — `BG1`, `BG2` — plus `input` and `specified_as`, and should carry `cannot_be_defaulted_because`. The id is required because other files cite these, and cited by ordinal position they silently move the moment anyone appends a gap: on the first live run three of four references in the brief ended up pointing at the wrong gap, so a blocker chased from the brief would have been reported to the wrong owner.

```json
{"assumptions": [{"id": "A1", "input": "slot length", "assumed": "20 minutes",
                  "because": "standard for this forum", "confidence": "material",
                  "changes_what": "the cut order and the Q&A budget"}]}
```

## findings.json

Written by the orchestrator, not by the critic — the critic's grant has no write tool, because a reviewer that can write can edit what it is judging. Transcribe its findings verbatim: all of them, in its order, in its words. Softening, merging, dropping or re-ranking a finding is a defect in the run, and the one most likely to go unnoticed, since the only party who could catch it is the one who did it.

Worst first. Each finding needs `id`, a `verdict` of CONFIRMED or SUSPECTED, `claim`, and `failure` — concrete inputs or state, then the wrong output. Add `severity` — a rank, where 1 is the worst finding in the run — an `anchor` with file, line or slide and the quote, a `direction` — severe where the piece asserts more than it can carry and passes silently, lenient where it undersells and costs effect but not standing — and `smallest_fix`. Anything you cannot anchor is dropped, not softened. `coverage` says what was reviewed; `not_reviewed` names what was skipped, because a review that does not say what it skipped is not a review.

```json
{"findings": [{"id": "F1", "verdict": "CONFIRMED", "severity": 1,
               "claim": "Slide 6 states a forecast as a result",
               "failure": "Reader reads 18% as achieved; it is modelled",
               "direction": "severe"}],
 "not_reviewed": ["appendix"]}
```

## The four rules that make these compose

**Cite the id of every candidate you lift into `artifact.md`.** Without it there is no mechanical way to check that the draft used kept material rather than refused material, and a reviewer has to match text by hand. On the first live run that is exactly how the worst finding hid: a refused entailment came into the draft as an unattributed sentence, so nothing prompted anyone to open its note.

**Only the writer writes prose for the piece.** Specialists deliver structured fields — a segment, a labelled claim, a charitable objection, a candidate line — not sentences for the deliverable. One voice in a multi-agent run is a property of who holds the pen, not of style guidance; four agents each producing polished paragraphs is how you get a stitched artifact with four registers in it. If a finding only makes sense as prose, compress it into its field and let the writer expand it.

**A disagreement between two specialists becomes an open choice, never a silent resolution.** Where your output contradicts another agent's — the primary segment against who actually blocks, an evidence gap against a claim the brief assumes — write it into `choices.json` as an open choice with a `conflict` block naming both agents in `between` and the substance in `about`. Do not adjudicate, do not average, do not quietly drop the weaker reading. This package's own defects came from exactly this being skipped: the resolution was invisible, so nobody could see a decision had been taken.

**Use `"unpriced"` where the literature states no cost.** Unpriced means unknown, not free. Never manufacture a trade-off to fill a field: an invented cost reads as a finding, which makes it worse than an admitted gap. Where the trade-off you state is your own judgement rather than a documented one, set `sourced: false` on that option, so it renders visibly differently from a sourced one. The same rule governs `stated_cost` in `objections.json`.

**Do not ask; default and record.** A forked or background agent has no return path, so a question does not pause the run, it ends it: the caller receives a question list where a deliverable should be. For every unknown input, take the defensible default, add an `assumptions.json` entry saying what was assumed, why, and what moves in the deliverable if it is wrong, and deliver complete work anyway. An input with no defensible default — a figure you would have to invent, a name only the principal holds — becomes a `blocking_gaps` entry whose `specified_as` states exactly what belongs there, and the writer places a marker at that point in `artifact.md`, written as `[gap: what belongs here, and who holds it]`. Never generic filler in place of a gap. This is `AUD-05` run where nobody can answer.

## Writing discipline

Write your file once, complete, at the end of your work — not incrementally. A half-written file is indistinguishable from a crashed agent's, and the panel may read the directory at any moment. Valid JSON, UTF-8, no trailing commas, no comments. **The schema rejects any field it does not define.** If you need one it lacks, that is a schema change to raise, not a field to invent: an undefined field is invisible to the panel, unchecked by CI, and indistinguishable from a typo. Seven were invented on the first live run and nothing surfaced any of them until the schema was sealed — six turned out to carry real decisions and are now defined, which is the outcome raising it would have produced immediately. **Prefix every id with its file, not just with your agent letter.** `CLM-3` for a claim, `OBJ-7` for an objection, `OPN-2` for an opening candidate, `ARG-11` for an argument, `ASM-4` for an assumption, `BG-2` for a blocking gap. Two files each minting `O1` is not hypothetical — it happened on the first live run, where `objections.json` and the opening set in `candidates.json` both used it, and `artifact.md` cited both fourteen lines apart. A cross-reference then resolves to a real entry in the wrong file and nothing is raised. The agent-letter prefix on the two shared files is a separate rule and both apply.

If you cannot fill a required field, keep the key and write `null` for a scalar or `[]` for a list, then record why in `assumptions.json`. Do not drop the key: an omitted field and an unanswerable one look identical afterwards, and only one of them is a finding. A file that falls short is visible and diagnosable; a missing file is indistinguishable from a specialist that never ran. On the two shared files, append; preserve every entry already there. Two rules make that survivable, and both exist because the first live run of this package broke without them.

**Prefix every id you mint on a shared file with your own letter** — `S` strategist, `E` evidence, `A` adversary, `I` invention, `W` writer, `C` critic — so a choice is `CH-E1` and an assumption is `AS-A3`. Specialists run in parallel and cannot see each other. Sequential ids collide, and a collision does not raise anything: the file stays valid JSON and one agent's entry is simply gone.

**Re-read the shared file immediately before you write it, never from a snapshot you took earlier in your run.** Another agent may have written it while you worked. Merge what is there with what you are adding, and if what you read has entries you have not seen before, that is the normal case rather than an error. This is a convention and nothing enforces it — there is no lock and the panel cannot supply one, so an agent that skips it silently deletes another agent's work.

## What this is not

If the author is running the local panel, it reads this directory and writes back exactly two things: a decided choice, moved from `open` into `decided`, and a corrected assumption, filled into `corrected_to`. Nothing else is touched, and it is the only writer here that is not an agent.

Nothing in the run depends on it existing. Switched off, you still have the run directory and `artifact.md`, and that is the deliverable. Never wait on a decision, never poll for one, never write a line that assumes anyone is watching. An open choice with `recommended` set is a finished output, not a pending one: the writer proceeds on it and states in `artifact.md` which way it went and what the alternative was.
