# Methods and decision model

The reasoning behind the package. `SKILL.md` is the operative text; this is the explanation of why it is shaped the way it is.

---

## PACT

The core loop.

| Step | What it establishes | The failure it prevents |
|---|---|---|
| **POSITION** | which audience, what change, what it costs them, what the occasion allows | a competent piece aimed at nothing |
| **ARCHITECT** | the form, the one governing idea, the structure, the evidential and emotional spine | a well-written list of topics |
| **CRAFT** | the words for the ear, the figures, the opening and close, the visuals | something that reads well and dies aloud |
| **TEST** | read aloud, timed, attacked, fact-checked, cut | a piece nobody stress-tested until the room did |

The ordering is the method. Almost every recoverable failure in this discipline is a step taken out of order — most often CRAFT before POSITION, which is unrecoverable by editing because the editing has nothing to edit *toward*.

## Design and Draft are separate modes

Five modes: Explain, Design, Draft, Review, Rehearse.

Design and Draft are split deliberately, against the convenience of merging them. Producing a plan and producing words are different tasks with different deliverables, and collapsing them produces the two commonest disappointments in this work: a plan handed over when words were needed, and words produced before anyone decided what they were for.

The rule the agent follows: **if the request says write, write.** If the request is ambiguous and the two would differ materially, produce the draft and state the plan in three lines above it.

## Proportional execution

The complexity of the response tracks the occasion, not the topic. A two-line toast loads no modules. A twenty-minute address to five hundred executives loads six and runs a boundary pass.

The mechanism: `SKILL.md` is preloaded; the twenty `references/*.md` modules load on demand; `audience-and-intent.md` is mandatory for any Design, Draft or Rehearse task and does not count against the discovery budget; one further primary module; then the boundary pass, which is not budget-limited.

The budget exists to stop a router from loading everything, which is the same failure as loading nothing — both produce generic output.

## Progressive loading, and why the boundary pass is separate

The boundary pass is a **separate step**, run after the primary module is chosen and before answering. It is not a filter applied to the request text.

That is the whole design point. A boundary is missed exactly when the request does not use its vocabulary. Nobody writes "please note this piece uses a non-rational mechanism" or "this audience is fatigued". They write "help me with a talk about our AI programme". Waiting to *notice* a boundary means never noticing it, so the pass asks the question about the situation rather than scanning for the words.

The ten boundaries are capped at ten on purpose. Adding an eleventh means removing one, and saying which. See `routing-checklist.md`.

## The form ladder

> one sentence said in person → an email or memo → a two-minute talk with no visuals → a talk with a handful of images → a fully narrated deck → a document plus a decision meeting → a repeated series → a campaign with owners and measurement

Use the first sufficient rung. Every rung up costs preparation, raises the failure surface, and lowers the audience's tolerance for being wrong.

This ladder makes real decisions rather than offering a metaphor. If a memo would persuade this audience better, the package says so and writes the memo. If the deck would be comprehensible without the speaker, it is a document and should not be projected. If someone asks for five dense slides, they want a document. Commencement, eulogy, apology, layoff, toast: no slides.

## Claim labelling

Every material claim carries exactly one type, and independently the status of its source:

`FACT` · `OBSERVATION` · `INTERPRETATION` · `FORECAST` · `HYPOTHESIS` · `ASPIRATION`

`CHECKED` · `UNVERIFIED` · `CONTRADICTED` · `RECHECK` · `NOT_APPLICABLE`

A type says nothing about whether anybody checked the claim, so `FACT` with `UNVERIFIED` is a real state and the common one.

The reason this is an invariant rather than a nicety: **most dishonesty in professional communication is not a false statement.** It is a forecast delivered in the grammar of a fact, a pilot described as a rollout, a capability described as a practice, an intention described as a result. All four survive fact-checking, which is exactly why fact-checking does not catch them and a label does.

The companion rule: whoever chose the comparison chose the conclusion. A number is input to a judgement, never output shopped after one.

## Mechanism selection by stated trade-off

Most persuasion runs on mechanisms rather than on arguments, and the same content built on a different mechanism produces a different result. So `MEC-01` is a **menu with costs**, not a permission list.

The format is the corpus's own — *when to use it, and what it costs* — because that is how the source literature states it: roughly six hundred such blocks across thirty-five of the thirty-eight works. This matters more than it sounds. An earlier draft of this module imposed a uniform grid (effect / speed / durability / second pass) across every mechanism, which produced a tidy table in which the sourced cells and the interpolated ones were indistinguishable. That is the defect `LOG-04` exists to catch, committed in the package's own documentation. The rule now: **where a trade-off is stated, a source states it; where the literature gives none, the entry is absent rather than filled.**

Three cross-cutting frames *were* stated as tables in the literature and are carried as such:

- **Durability.** A one-off prime holds for hours; a prime plus an expressed judgement until attention shifts; an active, chosen, effortful commitment for months; a cue at a recurring decision point indefinitely. Never rely on a prime for something you need next week.
- **Phase.** Cultivate → reduce uncertainty → motivate action. A mechanism fired in the wrong phase is the commonest reason a technically correct move reads as pressure — scarcity before trust is the classic.
- **Agitation or integration.** The primary division in the propaganda literature. Agitation is cheap, fast, indifferent to truth, and works on the poorer and less informed. Integration is expensive, slow, must look informative, and works *better* on the comfortable and educated. Where the objective genuinely is speed of conviction — an emergency, an outbreak, an evacuation — the agitation profile matches the job and its costs are being traded deliberately against an immediate one. The literature states that trade; it does not make it, and neither does the module.

The package's position is deliberate: **which mechanism is appropriate depends on context the package does not have, and the author does.** What the package owes is the menu and the documented costs. It does not pre-select.

`MEC-02` handles claiming to speak for a group, with a five-position cost scale for how a piece treats the people it does not speak for. Positions three and up buy compliance in the room and cost the information the author needed — sometimes a worthwhile trade in a mobilization, usually not in an organization that has to keep running.

`MEC-04` and `MEC-05` run the machinery in reverse, for reading someone else's message. Classify on four axes before judging; separate the facts from the intention and the interpretation; read for what action is requested rather than what belief is asserted; judge effect behaviourally; ask whether the outcome would have happened anyway.

## Activation, and why it is a module

A speech that ends in inspiration has no mechanism attached. The most common outcome of a good executive talk is enthusiastic agreement followed by nothing, and that outcome is designed in at the outline stage.

The distinctions `ACT` enforces:

| Not the same thing | And not the same thing |
|---|---|
| informing ≠ persuading | agreement ≠ adoption |
| persuading ≠ manipulating | a demo ≠ a proof |
| inspiring ≠ changing an organization | a pilot ≠ a capability |
| interest in a subject ≠ changed behaviour | a mandate ≠ a practice |

So the module supplies the mechanism: a commitment that is bounded, reversible, measurable, inside the person's own authority, and written by them; a first win that is planned rather than hoped for; a cascade chain with an owner per link; and a routinization sequence that runs after results rather than before them.

The test that decides whether an executive adoption piece is finished is not structural. It is whether a leader in the audience can answer five questions unaided: why the current approach is not enough, what is being asked of them specifically, which use case they will choose, who will own it, and how they will know whether it worked.

## Diagnosis before message

`CHG-01` runs three diagnoses before any communication intervention is designed, because most "communication problems" are not:

1. What looks like a **people problem** is usually a **situation problem.**
2. What looks like **laziness** is usually **exhaustion.**
3. What looks like **resistance** is usually a **lack of clarity.**

Then the test that actually discriminates: would they pass a pop quiz on what to do? If no, it is direction, and no amount of motivation helps. If yes and nothing happens, it is motivation or situation.

This is upstream of everything else. A better message aimed at a friction problem is wasted effort delivered confidently.

## The seven-question cap

The package never returns a question list instead of a deliverable.

Where an input is missing, it asks **at most seven** questions, ranked by how much the answer changes the work. Where the user cannot or will not answer, it takes the defensible default, states the assumption at the top of the deliverable, and produces the complete work anyway.

One exception: a factual claim that would otherwise have to be invented. There, the gap is named as the finding, and everything not depending on it is delivered in full.

The cap exists because a request for a talk answered with fourteen questions is a refusal wearing the costume of diligence.

## Review debt

Changing a number, an attribution, a claim, or a line someone will quote incurs review debt, discharged by calling `oratores-critic` on that change before the work is reported complete.

This is not self-verification. The critic runs with a fresh context and **no write tools**, so it can contradict the producer. Re-reading your own draft in your own context cannot, which is why doing that instead does not clear the debt.

Nothing outside the rule tracks that debt, so an uncalled review is silently lost. That is stated in the invariants rather than hidden, because a convention presented as a gate is the exact defect the critic is paid to find in other people's work.

## The audit, and what it found in this package

The package was audited against its own corpus and its own rules by seven independent passes: one on the architecture, one on internal coherence, and five over the thirty-eight source works. Roughly a hundred findings. The structural ones are recorded elsewhere in this file; the ones worth keeping here are the four where **this package broke the rule it exists to enforce**, because the same failure will be available to whoever extends it.

**A uniform grid over ragged evidence.** An earlier draft of `MEC-01` imposed effect / speed / durability / second-pass across every mechanism. Some cells came from books, some were interpolated so the table would not look ragged, and in the finished table the two were indistinguishable. Replaced with the corpus's own *when to use it, what it costs* form.

**A cost invented and labelled documented.** `MEC-02` carried "its documented cost: the flattery is easy to satirise". No source in the corpus says it. The adjective was doing the laundering: without *documented* it would have read as the guess it was. Replaced with the two costs the sources do state.

**A finding inverted.** `MEC-01` read "a saturated audience needs a stronger dose". The source says the opposite — content-indifference comes with heightened sensitivity to the stimulus, so the dose that fires a saturated audience gets *smaller*. The first half of the sentence was accurate and the inference from it was backwards, which is the hardest version to catch by reading.

**Effect sizes left bare in the module that forbids bare effect sizes.** "63% against 5%", "halves it", "triples follow-through" — all in the modules whose job is to stop exactly that. `LOG-04` and `SRC-01` state the escape and neither was used.

Three of the four are the same defect wearing different clothes: **something plausible presented in the grammar of something verified.** The rule that follows, and that the mechanism module now states in its own header: where a cost is stated, it is a documented one; where the literature gives none, the line is absent, and an absent line means unknown rather than free.

One more, of a different kind, because it hung a live run. The five fork skills carried a guard — *a forked context cannot ask the caller* — scoped to the opening move only. Mid-run, `AUD-05`'s seven-question gate fired anyway, the fork asked, and the work stopped with a question list where a deliverable should have been. `AUD-05`'s own failure signal is "a question list instead of a deliverable". The guard now covers the whole run, the router conditions asking on whether an answer can reach you, and `check_fork_question_gate` fails the build if a fork ever instructs asking again.

A fifth, found by the first agent that had to *use* the run schema rather than read it. `run-artifacts.schema.json` offered agents a controlled vocabulary — generators named `word-map`, `take-a-hike`, `defeated-expectation`, `contrast-pairs`, and lenses named `stasis`, `question-type`, `authority-source`. Nine of those terms appear in no module in this package. They came from a convergence pass across the corpus and they name real things, but the module that would define them is not written, so an agent filling the field had nothing to look up and could only guess at what the term meant. A closed list nobody can resolve is worse than no list, because the list looks authoritative. `generator` is a free string again, `lens` names the one lens `CHG-01` actually defines, and the vocabulary comes back when the module carrying it does.

The same pass pulled a bare figure out of the schema — an ask delivered at "80-90%" — for the reason above, and closed an ordering defect worth recording because it was invisible from either end. `findings.severity` was `integer, minimum 1` with no direction stated; the panel sorted ascending; the agent writing the sample run numbered 5 as worst. Every piece was internally consistent, and together they listed the critic's findings in exactly the reverse of the intended order, under a heading reading *worst first*. An unstated convention is not a convention.

## What executing it found that reading it had not

The multi-agent layer was designed, contracted, schema'd, given a panel and a hand-written sample run — and then run for the first time on a real brief. Everything below was invisible until it ran, and none of it is about the advice.

**Seven fields were invented by agents that the schema did not define, and nothing surfaced any of them.** `additionalProperties` was unset, so an invented field simply validated. Six turned out to carry real decisions — the proof-order record, the answer to `PTH-05`'s test, the occasion's timing budget — and are now defined, taking the agents' own names rather than better ones, because the run is evidence of what the work needs. The seventh duplicated a field belonging to another file, under the same name, with different semantics: `checked_first` in one file meant the order a hostile reader attacks in, and in the other the order somebody should go and check. One name across two meanings hid that a verification owner and a Q&A rehearsal were working from different lists. The schema now rejects any field it does not define, at every level.

**Ids drifted, silently, in the direction that is hardest to notice.** Blocking gaps were cited by ordinal position; appending a gap shifted three of four references in the brief onto the wrong gap. A blocker chased from the brief would have been reported to the wrong owner. Separately, two files each minted `O1` — one for objections, one for opening candidates — and the draft cited both fourteen lines apart, so a cross-reference resolved to a real entry in the wrong file with nothing raised.

**Three agents append to two shared files with no lock.** Sequential ids collide and the loser is overwritten rather than erroring. It did not bite only because one agent happened to re-read before writing and noticed. The rule now is an agent-letter prefix and a re-read immediately before the write, and the honest note beside it is that nothing enforces either.

**The contract assigned a file to an agent that has no tool to write it.** The critic's grant withholds `Write`, `Edit` and `Bash` deliberately, and that is the one property here enforced by mechanism rather than instruction. The contract said it wrote `findings.json`. The contract yielded: the critic authors, the orchestrator transcribes verbatim, and the manifest gained `authored` alongside `writes` so it no longer asserts a write that cannot happen. The weakness is stated where it can be read — the reviewed party holds the pen on the review, and nothing detects a softened finding.

**And the writer contradicted itself nine lines apart.** The draft said *I cannot stand here and tell you the pilots failed* and then used a kept metaphor asserting exactly that. It survived the writer, who had every file in front of it. It was caught by the critic, whose whole value is having no stake in the draft — and it was invisible partly because the draft cited ids for four of the eleven candidates it used, so nothing prompted a reader to open the note that ruled that entailment out.

The pattern across all six: **every one is a place where two things that were separately correct were never checked against each other.** That is what an execution finds and a reading does not, and it is why the sample run written by hand contained none of them.

## What the second review found, which is worse

The revision that discharged those twenty-five findings was reviewed again by the same critic on a fresh context. It confirmed eleven fixes, called five partial, and found four claimed as discharged that were not. It also produced twenty new findings, and **four of them were caused by the fixes.**

That is the part worth keeping. Not that a first draft has defects — that is ordinary. That **a fix, written by the party that caused the defect, with the finding in front of it, reliably introduces a new one nearby.**

Four examples, all mine:

- A finding said an objection was conceded with no owner named, because the owner sat inside a bracketed writer's note the audience would never hear. The fix moved it into the spoken text and, filling the sentence out, added a location, a request the speaker was said to have made, and a consequence for leadership's silence — three checkable claims that appear nowhere else in the run, on the sentence carrying the piece's one genuine concession.
- A finding said the piece named four alternatives it never listed. The fix listed four. They were not the run's four: the two that would have cost the talk something were dropped, one was substituted from a candidate whose own note calls it *the innocent cause that would account for the damaging appearance*, and a fifth nobody had advanced was added so that eliminating it looked like progress. A concession that concedes nothing expensive is worse than none.
- A finding said a gap marker was missing under a blocked section. The fix added a conforming marker asserting there was no fallback for the close — while the file the marker cites records one, chosen precisely for the case where that gap never lands.
- And the one against this document's own subject: a finding said the manifest could not distinguish a completed stage from one that never ran, because its timestamps were filled in one pass. The fix told every agent to write its own. That contradicted the rule that the manifest has a single writer, and the manifest carries neither the append discipline nor the id prefixes that make a shared file survivable — so a bookkeeping defect became a concurrency defect on the run's own record of itself.

The pattern under all four is the pattern from the first run, one turn later: **two things separately correct, never checked against each other.** A fix is written against the finding, and the finding is a paragraph, not the whole run.

What follows for the package is not a new rule to obey. It is why the critic holds no write tool, and why that is the one property here enforced by mechanism. A producer that could apply its own review would apply it the way these four were applied — locally, plausibly, and with a new defect in the neighbourhood — and would then report the debt discharged, in a table, in the file it wrote. That table is now the record, and the party that wrote it is the party being audited. Nothing in the package detects a false row in it. The second review is the only thing that did.

## The second filter, and why there is not one

A package like this has an obvious-looking safety move available: document the ugly mechanisms, then add a gate that refuses them. It costs one line per module and it reads as responsible.

It is the wrong move, and the reason only becomes visible once you notice where the first filter already is. The model running this package carries its own refusal layer, and that layer applies itself without being asked. A gate inside the skill adds nothing to it. What it adds is a *second authority to decline under* — and what gets declined is not harm, it is method. The mechanism goes missing before anyone has decided whether to use it.

The failure is invisible from outside, which is what makes it expensive. A model that trims a procedure does not announce the trim. It returns a complete-looking answer with the uncomfortable half absent, and the author cannot tell a full answer from a reduced one. That is this document's own recurring defect pointed the other way: not plausible material in the grammar of verified material, but partial material in the grammar of complete material.

So the package holds two things, and neither is a moral position:

- **Do not fabricate evidence.** A peer who did not adopt, a deadline that does not exist, a statistic with no source. Those are false statements about the world rather than techniques, and the difference is not one of degree.
- **Do not present one kind of claim as another.** A forecast in the grammar of a fact, a pilot as a rollout, a claim's type softened to cover a source nobody checked.

Everything else is named, priced where a source prices it, marked `unpriced` where none does, and handed to the author. `MEC-01` documents the mechanisms that work best on the poorer and less informed, and states what each costs if it is named out loud. It does not decide, and it says so in its own words: the literature states the trade; it does not make it, and neither does this module.

Three places had drifted from that and were corrected. `PTH-05` gated on a test its own text calls imperfect — a gate cannot turn on a test the module admits is not decisive, so it now requires the question to be asked and its answer written down beside the decision taken. `EXE-01` forbade manufactured urgency while `DLV-02` taught raising it deliberately with syntax: two modules opposite on one word. The rule belongs on the *claim* — an invented deadline is a false statement — not on the intensity. And the fear rule was written as a prohibition when it is a finding about efficacy: fear without a way out fails because the audience defends itself against the message instead of acting on it, not because it is unfair. An efficacy finding written in the grammar of a prohibition is the same laundering as an invented cost written in the grammar of a documented one.

## What is mechanical and what is not

Two things are enforced by mechanism:

1. **The critic's tool grant.** No `Write`, no `Edit`, no `Bash`. A tool never granted is a mechanism; a filter over commands is best-effort, and `validate_skill.py` fails the build if the grant drifts.

   That claim was false for most of the day this package was built, and the way it was false is worth more than the claim. The critic's frontmatter carried `memory: user`. Setting `memory:` to any value makes the harness enable `Read`, `Write` and `Edit` automatically, so the subagent can manage its own memory files — which bypasses the `tools` allowlist entirely. So the one property here described as mechanical rather than conventional was, in fact, neither: the tool was granted and nothing said so.

   The validator did not catch it, and could not have: `check_critic_tool_grant` read `tools:` and asserted the absence of write tools there, while the widening came from a field four lines below that nothing looked at. **A check that reads one field and concludes something about the whole grant is a check that reports what it examined as though it had examined the thing.** The suspicion was raised early and set aside, because confirming it needed a restart and the field also appeared in a working package elsewhere — which is a bad reason, and the same bad reason as *it validates, so it is correct*. It was settled by reading the documentation, which took four minutes.

   The field is gone, the reason is written into the critic's own file where the next person to add it will read it, and `validate_skill.py` now fails the build if `memory:` reappears — tested by reintroducing it on a copy. Persistent memory and a withheld write tool are mutually exclusive, and the withheld tool is the one worth keeping.

   Checked at the same time and found true: `skills:` in agent frontmatter preloads the named skill's `SKILL.md` and **only** `SKILL.md`. The `references/*.md` modules and the scripts load on demand. Every agent in this package asserts that about itself, six times, and it is accurate.
2. **The validators.** Structure, addressing, countability, boundary count, index coverage in both directions, fork wiring.

Everything else — the module budget, the boundary pass, the seven-question cap, the claim labels — is a convention a model follows. It can be declined.

The package does not police what is written. The one thing it holds to is not fabricating evidence: an invented statistic, study or benchmark is false work product, and separately it is the fastest way to lose a room. Everything else is a trade-off with its costs attached, weighed by the author.

And the limit worth stating plainly: nothing here can verify that a claim in a delivered piece was true, that a cited peer really adopted, or that an audience could in fact disagree. Those are properties of the world, checked by people. The package can require that they be checked. It cannot check them.
