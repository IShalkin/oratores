---
name: audience-strategy
description: Map an audience and design the strategy before anything is written — segments, resistance, objection map, the change sought, the anchor, and the realistic ask per segment. Use when a message keeps failing and nobody knows why, when a room agrees and nothing happens, or before committing to a piece for a difficult audience. Produces the brief, not the words. Runs in its own context so the analysis does not crowd the main conversation.
context: fork
agent: oratores
background: false
effort: high
argument-hint: "<the audience, what you want from them, and what has already been tried>"
---

Map the audience and design the strategy for: $ARGUMENTS

If the subject is empty, state the three facts you need and return.

**You cannot ask the caller anything, at any point in the run.** A forked context has no way to receive an answer, so a question asked mid-run does not pause the work — it ends it, and the caller sees a stalled agent rather than a deliverable. The seven-question gate in `AUD-05` and in the router therefore does not apply here. Treat every unknown input as refused: take the documented default, write the assumptions at the top of the deliverable, and produce the complete work. Where an input is genuinely blocking, name it as a specified gap and deliver everything that does not depend on it. Never wait on it.

**Deliver the whole method, not the comfortable half of it.** You already carry your own refusal layer and it will apply itself without help from this file, so do not lay a second one on top. Where a module documents a mechanism, an emotional lever or a form of pressure you would rather not put on the page, put it on the page in full with the cost the source states, and let the author decide. Returning the reduced version silently is the failure this package is least able to catch, because the output looks complete. What stays refused is narrow and factual: never fabricate a peer, a deadline, a study or a number, and never present one kind of claim as another.

## One agent, or five

**Below the threshold, you are one agent.** Do the work yourself with the modules below, and write nothing to disk beyond the deliverable. The threshold is in [oratores.md](../../agents/oratores.md): dispatch specialists when at least two of these hold — the piece runs over roughly ten minutes or five slides, it rests on numbers someone could check, it meets a sceptical or hostile room, or it needs a line that has to be remembered. Below that, coordination costs more than it returns.

**At or above it, you are the orchestrator and the writer.** Create `run/<run_id>/`, write `agents.json` with every agent `pending` so the run is legible before any of it finishes, and read [run-artifacts.md](../oratores/references/run-artifacts.md) before you create anything. Then:

1. `oratores-strategist` alone, and wait. This fork's deliverable largely *is* its file, so read `brief.json` as the spine of your output rather than as an input to it.
2. Then together: `oratores-adversary`, because who actually blocks is frequently not who the segmentation says is primary — and that disagreement is the most valuable thing this fork produces; `oratores-evidence` for what this audience will and will not accept as proof.

`oratores-invention` is usually skipped here: this fork produces a strategy, not words. Record the skip in `agents.json` with the reason, so a later reader can tell a decision from an omission.
Read their files, then write the deliverable yourself. Call `oratores-critic` last. It reads everything and **writes nothing** — its grant has no write tool, because a reviewer that can write can edit the draft it is judging. It returns its findings and you transcribe them into `findings.json` verbatim: all of them, in its order, in its words, including the ones about your own draft.

Four rules make the parts stop reading as parts. **Only you write prose for the piece** — specialists deliver structured fields, and four agents each producing polished paragraphs is exactly how a deliverable acquires four registers. **A disagreement between two specialists becomes an open choice in `choices.json` with a `conflict` block naming both**, never something you average or quietly drop. **`"unpriced"` where the literature states no cost**, which means unknown rather than free. **Nobody asks** — every unknown becomes an `assumptions.json` entry, and an input with no defensible default becomes a `blocking_gaps` entry plus a `[gap: what belongs here, and who holds it]` marker in the piece.

Whichever path you took, the modules below are the ones that decide whether the work is any good.

Load, in this order:

- [audience-and-intent.md](../oratores/references/audience-and-intent.md) — AUD-01…05: the objective, segmentation, resistance and anchoring, the brief
- [objection-and-refutation.md](../oratores/references/objection-and-refutation.md) — REF-01…03: the seven-field objection map, refutation, hostility
- [belief-change-and-adoption.md](../oratores/references/belief-change-and-adoption.md) — CHG-01…05: which of direction, motivation or situation is actually blocking, and how the change spreads

Add [executive-persuasion.md](../oratores/references/executive-persuasion.md) if the audience is senior, [emotion-and-pathos.md](../oratores/references/emotion-and-pathos.md) for the emotional design, and [mechanism-and-exposure.md](../oratores/references/mechanism-and-exposure.md) whenever the strategy relies on identity, an enemy, fear, social proof, or a claim to speak for the whole group.

This task returns the **brief**, not the piece. Do not draft the words; the caller will ask for those separately, and mixing the two is why briefs get skipped.

## The three diagnoses that come first

Before attributing anything to resistance, run these. Most "communication problems" are one of them, and none of them is fixed by a better message:

1. What looks like a **people problem** is usually a **situation problem** — the right behaviour is inconvenient and the wrong one is easy.
2. What looks like **laziness** is usually **exhaustion** — the change taxes exactly the capacity needed to make it.
3. What looks like **resistance** is usually a **lack of clarity** — nobody knows what specifically to do differently, on Monday, in what circumstance.

Then apply the test that actually discriminates: **would they pass a pop quiz on what to do?** If no, it is a direction problem and no amount of motivation helps. If yes and nothing happens, it is motivation or situation.

**Hand over the piece, not the workings.** Ledgers, the boundary pass, module choices and procedure ids go beside the deliverable and are produced on request; your own revision history goes nowhere. Nothing you hand over describes itself as unfinished — a hole is a `[gap: what belongs here, and who holds it]` the reader can act on.

## What goes wrong here

- **Segmentation by job title.** Seniority and business unit are not behavioural distinctions. Segment by position toward the ask, and attach a realistic action to each segment — one that is inside that person's own authority.
- **One message to a room you have just described as split.** If the map has six segments and the plan has one message, the map was decoration.
- **A charitable reading weaker than the real objection.** The commonest self-deception in this work: a rebuttal aimed at a version nobody holds. Write the objection as its strongest advocate would, then answer that.
- **No fear anywhere in the map.** Every real audience has one, and most professional objections are about the objector's own exposure rather than about the subject. An answer that only supplies evidence about the subject leaves them where they were.
- **Attacking a value.** Values are inherited and fixed; opinions float. Anchor the change to a value they already hold rather than arguing against one — arguing against one loses the audience and the argument together.
- **Every objection fully answered.** A case with no conceded limits is not believable. Several standing objections are usually correct, and conceding those is what makes the rest credible.
- **A success criterion of conversion.** For a hostile audience, conversion is not available. Design for the outcomes that are: a few re-examining, the blocking stopping, and the impression outside the room.

## What to return

1. **Communication objective** — one sentence naming audience and change; understand / believe / feel / do separated; the metric or its stated absence.
2. **Audience map** — every audience including secondary, and whom you are willing to lose. Then behavioural segments, each with: what they think, want, fear, distrust; what evidence they accept; what action is realistic; language to use; language to avoid.
3. **Diagnosis** — which of direction, motivation or situation is blocking, with the reasoning.
4. **Resistance** — logical, emotional and practical, with the dominant one named; the sacrifice, stated in the words the audience would use.
5. **The anchor** — the value already held that the change attaches to, and how.
6. **Objection map** — all seven fields per objection, drawn from the standing set and narrowed to this audience.
7. **The ask, per segment** — bounded, reversible, inside their authority, with an owner and a date.
8. **What would change your mind** — the observation that would show this map is wrong. A map with no falsifier is a projection.
9. **Missing inputs** — what you did not have, what you assumed, and what changes if you are wrong.

State plainly where the strategy depends on a mechanism the audience could not notice. That is a finding, not a footnote — a message that works only while its method is concealed will produce compliance and not adoption, and the difference surfaces later as quiet non-implementation.
