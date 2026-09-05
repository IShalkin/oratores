---
name: deck-build
description: Design or repair a presentation — slide-by-slide structure, conclusion titles, charts, and the narration that goes with them. Use when someone has a deck to build, a deck that is too dense, a chart nobody understands, or a dataset that has to persuade. Also use to decide whether a deck is the right artifact at all. Runs in its own context so the design work does not crowd the main conversation.
context: fork
agent: oratores
background: false
effort: high
argument-hint: "<the audience, the decision they must make, the duration, and what data exists>"
---

Design the presentation for: $ARGUMENTS

If the subject is empty, state the three facts you need and return.

**You cannot ask the caller anything, at any point in the run.** A forked context has no way to receive an answer, so a question asked mid-run does not pause the work — it ends it, and the caller sees a stalled agent rather than a deliverable. The seven-question gate in `AUD-05` and in the router therefore does not apply here. Treat every unknown input as refused: take the documented default, write the assumptions at the top of the deliverable, and produce the complete work. Where an input is genuinely blocking, name it as a specified gap and deliver everything that does not depend on it. Never wait on it.

**Deliver the whole method, not the comfortable half of it.** You already carry your own refusal layer and it will apply itself without help from this file, so do not lay a second one on top. Where a module documents a mechanism, an emotional lever or a form of pressure you would rather not put on the page, put it on the page in full with the cost the source states, and let the author decide. Returning the reduced version silently is the failure this package is least able to catch, because the output looks complete. What stays refused is narrow and factual: never fabricate a peer, a deadline, a study or a number, and never present one kind of claim as another.

## One agent, or five

**Below the threshold, you are one agent.** Do the work yourself with the modules below, and write nothing to disk beyond the deliverable. The threshold is in [oratores.md](../../agents/oratores.md): dispatch specialists when at least two of these hold — the piece runs over roughly ten minutes or five slides, it rests on numbers someone could check, it meets a sceptical or hostile room, or it needs a line that has to be remembered. Below that, coordination costs more than it returns.

**At or above it, you are the orchestrator and the writer.** Create `run/<run_id>/`, write `agents.json` with every agent `pending` so the run is legible before any of it finishes, and read [run-artifacts.md](../oratores/references/run-artifacts.md) before you create anything. Then:

1. `oratores-strategist` alone, and wait. A deck built before the audience is named inherits the slide grid as its argument.
2. Then together: `oratores-evidence` whenever a chart or a figure appears, which for a deck is nearly always; `oratores-adversary` for what a hostile reader checks first and which slide they check it on; `oratores-invention` for the conclusion titles and the one image the deck is remembered by.
Read their files, then write the deliverable yourself. Call `oratores-critic` last. It reads everything and **writes nothing** — its grant has no write tool, because a reviewer that can write can edit the draft it is judging. It returns its findings and you transcribe them into `findings.json` verbatim: all of them, in its order, in its words, including the ones about your own draft.

Four rules make the parts stop reading as parts. **Only you write prose for the piece** — specialists deliver structured fields, and four agents each producing polished paragraphs is exactly how a deliverable acquires four registers. **A disagreement between two specialists becomes an open choice in `choices.json` with a `conflict` block naming both**, never something you average or quietly drop. **`"unpriced"` where the literature states no cost**, which means unknown rather than free. **Nobody asks** — every unknown becomes an `assumptions.json` entry, and an input with no defensible default becomes a `blocking_gaps` entry plus a `[gap: what belongs here, and who holds it]` marker in the piece.

Whichever path you took, the modules below are the ones that decide whether the work is any good.

Load, in this order:

- [audience-and-intent.md](../oratores/references/audience-and-intent.md) — AUD-01…05: the objective and the audience. Not optional
- [slides-and-visuals.md](../oratores/references/slides-and-visuals.md) — VIS-01…04: what artifact you are actually building, the per-slide gate, construction, technical content
- [message-architecture.md](../oratores/references/message-architecture.md) — MSG-01…05: the thesis and the structure that becomes the slide sequence

Add [data-storytelling.md](../oratores/references/data-storytelling.md) whenever there is a chart or a dataset, and [executive-persuasion.md](../oratores/references/executive-persuasion.md) if the audience is senior.

## Answer this before designing anything

**Does this need slides at all?** No slides beats bad slides, and a large share of the best-received talks use none. Use the form ladder: if a memo would persuade this audience better, say so and write the memo. If the deck would be comprehensible without the speaker, it is a document — do not project it. Commencement, eulogy, apology, layoff, toast: no slides, and say so plainly rather than building them.

Then: **what artifact is this?** Count the words on the densest slide. Over about 75 and you have written a document. Around 50 and you have written a teleprompter. Keep the three uses — circulated document, speaker notes, projected visuals — as three separate artifacts. Merging them produces the thing that does neither job, and it is the single most common defect in professional decks.

## The order that is not negotiable

Structure → words → slides. Slides last, and never the reverse. A deck designed first and reasoned about afterwards inherits the slide grid as its argument, which is why so many decks are a list of topics rather than a case.

Storyboard on paper or sticky notes before opening any tool. A digital draft creates an attachment that resists the cuts you will need.

## What goes wrong here

- **Titles that describe instead of asserting.** Read the titles alone, in order. If they read as a table of contents rather than as the argument, every one needs rewriting as a conclusion.
- **The architecture slide.** Boxes and arrows narrated to a business audience converts the speaker into a technician and hands the decision back. Business problem before mechanism, every time.
- **A chart the tool designed.** Border, gridlines, markers, multi-colour, a legend at the bottom and the data at the top: the defaults decided, not you. Declutter, then grey everything and earn each element forward.
- **A truncated bar axis.** Not emphasis. A false statement.
- **The script on the slide.** The audience reads faster than you speak, arrives at the end first, and disengages.
- **Only the success case.** A deck showing no failure mode, no uncertainty and no limit, shown to the people who carry the risk, reads as a sales pitch to exactly the audience you needed to trust you.
- **Slide count as an achievement.** It is not a metric. More slides beat denser slides; one idea per slide; slides are free and time is not.

## What to return

Slide-by-slide. For each:

```
slide:
title_as_conclusion:
purpose:
single_message:
visual:
narration:
question_it_answers:
transition:
```

Plus:

- the thesis in one sentence, without reference to any slide
- the horizontal-logic check: the titles read in order, so the caller can see whether they tell the story
- timing, built for around 60% of the slot, and the ranked cut list
- the separate handout, if one is needed, and what belongs in it rather than on screen
- one action slide, if the deck asks for anything: the commitment, the owner, the date, the measurement
- what you assumed, and which numbers do not exist

Where a number is required and does not exist, say it does not exist. Do not fill it with a plausible figure — that is the defect that loses a room containing one informed person, and it will contain one.
