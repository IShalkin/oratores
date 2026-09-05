# Usage patterns

Reusable prompts and what each returns. Everything here works with the router; the fork skills are for when you want the analysis kept out of the main conversation.

For anything short, this is a conversation with one agent and there is nothing to manage. For a real piece it splits across six agents writing files into a run directory — see *When it becomes six agents* below. You do not have to ask for that; the threshold is in the package and it is meant to decide for itself.

---

## Choosing where to send a request

| You have | Use | Why |
|---|---|---|
| A question about rhetoric or persuasion | the router, Explain mode | one module, a direct answer |
| An occasion and no plan | `audience-strategy` | returns the brief, not the words |
| A brief and no text | `speech-draft` | returns text a person can deliver |
| Slides to build or repair | `deck-build` | decides first whether slides are the right artifact |
| A draft to check before it ships | `persuasion-audit` | findings anchored to lines, no rewriting |
| Someone else's message to understand | `persuasion-audit` | classifies before judging; analyzes all sides equally |
| A senior audience that agrees and hasn't moved | `exec-activation` | returns the full activation system |
| A line, a metaphor or an opening and no idea where to start | the router, and ask for candidates | `INV-03` runs the generators instead of waiting for arrival |
| Anything small | just ask | a two-line toast loads no modules |

---

## Design

```text
Use $oratores to design a 20-minute talk. Audience: about 500 managing
directors and country heads. They've heard about AI for two years, they agree it
matters, and almost nothing in their business units has changed. I need them to
each pick one workflow and name an owner. Design it — don't write it yet.
```

Returns: the objective (understand / believe / feel / do, separated), behavioural segments with a realistic action each, the thesis in one sentence, the structure with each section's logical and emotional function, the evidence plan, the objection map, and the ask. Plus what it assumed.

```text
I have to announce a reorganization to 200 people, half of whom think it's aimed
at them. Map the audience and tell me what the message has to do before it can
say anything about the structure.
```

Returns: the audience map, the dominant resistance, the sacrifice named in the words the audience would use, the value to anchor to, and the ask per segment. It will also tell you if the real problem is that the reorganization is bad, because that is a performance problem and no message fixes it.

---

## Draft

```text
Write it. 20 minutes, so about 2,200 words. The speaker is our regional head —
plain, unrhetorical, hates anything that sounds like a keynote. She can't land
a joke. Open by acknowledging that everyone is sick of hearing about this.
```

Returns: the text, laid out in phrases if it will be read, with pauses marked. Plus the thesis in one line, the timing at delivery pace, the ranked cut list, and what was deliberately left out.

```text
Rewrite this so it works aloud. It reads fine and dies when I say it.
```

Returns: the rewrite, plus what was wrong — usually sentences that fail the breath test, abstractions where something concrete was needed, and the strongest word buried in the middle of a sentence rather than at the end.

```text
Talking points for a 10-minute slot I might not get. Give me the 3-minute version
and the 1-minute version too.
```

---

## Review

```text
Review this deck before it goes to the board. Don't rewrite it — tell me what
they'll push back on and where.
```

Returns: findings worst-first, each anchored to a slide, each with the concrete failure and the direction of failure (does a bad deck pass, or a good one fail?), and the smallest fix. Then what was checked and found clean, so the coverage of the review is visible.

```text
What's actually doing the work in this draft, and what does each move cost me?
```

Runs `MEC-01` and `MEC-03`: which mechanism carries each passage and what it costs, which claim a hostile reader checks first, and which numbers are unsourced.

```text
This campaign is being run at us. Explain how it works.
```

Runs `MEC-04`: classifies on four axes before judging, separates the facts from the intention and the interpretation, reads for what action is requested rather than what belief is asserted, identifies the source including the laundering check, and asks whether the outcome would have happened anyway. Analyzes all sides by the same standard.

---

## Rehearse

```text
I deliver this Thursday. Give me the delivery pack.
```

Returns: the marked script, the timing plan with the ranked cut list and both endings, the Q&A sheet including the hostile question and the one nobody will ask aloud, the technical contingency, and only the delivery notes that differ from default.

```text
Q&A prep. Assume the three most senior people in the room think this is a
distraction from delivery.
```

---

## Activation

```text
/exec-activation 500 MDs at the annual leadership meeting, 20 minutes plus 10 for
questions. Subject is AI adoption. They agree with it and nothing has changed.
I need commitments, named owners, and a way for it to cascade into the units.
```

Returns the twenty sections the playbook specifies, in order: strategic brief, audience map, objective, thesis, message architecture, structure, opening options with their risks, narrative, technical explanation, objection map, evidence plan, leadership commitment, cascade, slide-by-slide, delivery plan, rehearsal plan, Q&A, risk and exposure review, quality assessment, missing inputs.

It will tell you if the one blocking input is missing: **a real workflow, in this audience's own work, with a real friction and a real measurement.** Everything else has a defensible default; that does not, and a generic capability description produces exactly the talk they are tired of.

---

## Slides and data

```text
Should this be a deck at all? 30-minute slot, audience is four analysts who will
read anything I send in advance.
```

Often the answer is no, and the package says so and writes the memo instead.

```text
Build the deck. One idea per slide, conclusion titles, and one action slide at
the end with the commitment on it.
```

```text
This chart is correct and nobody understands it. Fix the chart, not the data.
```

Returns the redesign plus what was wrong. The usual answers: the tool's defaults decided the design, hue was used to encode quantity, or the title described instead of asserting.

```text
Turn this dataset into a five-minute story for people who won't read the appendix.
```

---

## When it becomes six agents

Above a stated threshold — roughly over ten minutes or five slides, resting on checkable numbers, meeting a sceptical room, or needing a line that has to be remembered — the work stops being one agent's. What you get back changes shape, so it is worth knowing what to expect.

A directory appears at `run/<id>/`. In it: the brief, the labelled claims, the objection map, the unfiltered candidates, the open decisions, the recorded assumptions, the critic's findings, and the draft. Four specialists produce the structured parts and **one agent writes all the prose**, which is why the piece does not read as four people taking turns.

Three things in there are worth opening before you read the draft.

**`choices.json` — the open decisions.** Where two constructions produce genuinely different results, both are there with the cost each source states. `"unpriced"` means the literature gives none, which is unknown rather than free. `sourced: false` means the trade-off is the agent's judgement rather than a documented one. And where two specialists disagreed, the disagreement is an open choice with both their names on it rather than something quietly resolved — on the first real run, six of eighteen decisions were that kind, and they were the six worth reading first.

**`assumptions.json` — what was defaulted.** A specialist has no way to ask you anything mid-run: a question emitted from a forked context does not pause the work, it ends it. So nothing asks. Every unknown becomes an entry saying what was assumed, why, and what moves in the deliverable if it is wrong. Some are marked `blocking`, meaning the piece stands on them. Correcting one and re-running that agent is the cheapest intervention available to you.

**`findings.json` — the critic's review.** Worst first, each anchored to a line, `CONFIRMED` separated from `SUSPECTED`, and a named list of what it did *not* review. The critic holds no write tool at all, so it cannot fix what it finds, and it cannot quietly improve the draft it is judging.

An optional local panel renders all of this — `python ui/server.py` — and writes back exactly two things: a decided choice and a corrected assumption. Nothing in the package needs it running. With it off you still have the directory and the draft, and that is the deliverable.

## Prompts that get better answers

- **Name the duration.** It changes everything downstream, and a piece built for the wrong length cannot be trimmed into the right one.
- **Say what the audience already thinks.** Not their job titles — what they believe, and what they have already heard on the subject. This is the single most useful thing you can supply.
- **Say what you want them to do**, specifically enough that you would know whether it happened.
- **Say what the speaker is like.** Register, what they can and cannot pull off, whether they can land a joke.
- **Say what evidence actually exists**, and say which numbers do not. The package will not invent one; you get a named gap with who would have to supply it, and the claim keeps its type while its source status reads `UNVERIFIED`.
- **Say whether you can answer follow-up questions.** In a conversation it will ask up to seven, ranked by how much the answer changes the work. In a fork or a background run it cannot receive an answer, so it asks nothing and defaults instead — which is better output if you were not going to be there, and worse if you were.
- **Say if you want a plan or the words.** If you do not, you will get the words with the plan in three lines above them.

## What it will tell you rather than decide for you

Where a choice has real trade-offs, you get both options with their costs rather than one silent pick:

- Two constructions that produce different effects, each with the trade-off its source states.
- A mechanism that is strong and short-lived, next to one that is weaker and holds.
- A move that works now and hardens a division you may need un-hardened later.
- Two kinds of doubt about a claim, kept apart: what kind of assertion it is — fact, observation, interpretation, forecast, hypothesis, aspiration — and whether anybody checked the source. A fact nobody checked is recorded as exactly that, rather than softened into an opinion to cover the missing check.

Ask for it directly if you want it foregrounded: *"give me two versions — the one that lands hardest and the one that survives being checked, with what each costs."*

## The one thing it will not do

Invent evidence. A statistic, study, benchmark or return figure that does not exist will be named as a gap, with who would have to supply it — not filled with a plausible number. That is not a restriction on your argument; it is the difference between a claim and a liability, and a room of five hundred contains one person who checks.
