# Message Architecture — MSG

The governing idea, and the structure that carries it. This module runs after `AUD-01` and before any prose. Its whole purpose is that controlling the order in which ideas arrive is the single most important act in making a message clear — and that no amount of good writing repairs a bad order.

---

## MSG-01 — The governing thesis

**Trigger.** Before any content is generated. Then again as the filter for every cut.

**Procedure.**

1. Write **one complete sentence** containing (a) your point of view and (b) what is at stake for this audience. Not a topic. Not a category.
   - Topic: "Workflow software."
   - Point of view: "We should update the workflow software."
   - Thesis: "Your department will miss its production deadlines until the workflow software is replaced."
2. Constrain it. A usable thesis is short enough to be repeated by someone who heard it once, contains a subject that is a version of *you* (the audience) and an active verb, implies a decision, and is not interchangeable with the generic version of itself.
3. Run the tests:

   ```
   Can it be said in one sentence, without a slide?
   Can someone in the audience repeat it accurately to their own team tomorrow?
   Does it imply a decision, rather than an attitude?
   Does it distinguish action from passive agreement?
   Does it survive deletion of every fashionable word in it?
   Would the opposite be a position someone reasonable could hold?
   ```

   The last test is the strongest. If nobody could disagree, you have a platitude, and no structure will rescue it.
4. Use it as the **filter**. Content that does not serve the thesis is cut, including content you like. If you do not filter, the audience must — and they will resent it.
5. **Do not repeat the same idea in five registers and call it a thesis.** One dominant melody; a piece may have three movements.

**Gates.**
- One sentence, point of view plus stakes, stated without a visual.
- Passes the repeatability and the disagreeability tests.
- Every section of the eventual outline traces to it.

**Failure signals.**
- "The purpose of this presentation is to…" — there is no message; go back to `AUD-01`.
- "There are three problems." "We recommend five changes." These name the *kind* of idea instead of its content, and they conceal incomplete thinking from you as much as from the audience.
- Any of: "AI will change everything", "the future is already here", "we stand at the threshold of a revolution", "digital transformation is no longer optional". These are placeholders where a thesis should be. Replace each with a specific workflow, a specific decision, and a specific consequence.
- You need the deck open to say what the piece is about.

---

## MSG-02 — Unbury the lead; find the counter-intuitive core

**Trigger.** Every piece. Mandatory when the thesis sounds like common sense.

**Procedure.**

1. Ask the telegraph question: if the line were cut after one sentence, what did you send? Invest disproportionate time in that sentence.
2. Find what is **counter-intuitive** about the thesis — the implication the audience has not drawn, or the reason it is not already happening — and lead with that. Common sense is the enemy: an idea the audience can predict does not register at all.
3. Surprise must be **post-dictable**: unpredictable before, obvious after. Surprise that yields no insight is a gimmick and costs more than it buys.
4. Prefer a **useful approximation to a useless truth.** Accuracy carried to the point where nobody can act on it is not rigour; it is a failure to translate.
5. Where the concept is genuinely new, transfer a schema the audience already owns and state only the delta. Prefer a **generative** metaphor — one that keeps answering questions you never briefed — over a decorative one. Test it by applying it to a situation you did not plan for; if it gives no guidance, replace it.
6. Where the audience has not a gap but an **abyss** — no relevant knowledge at all — supply context first. Curiosity requires something to be curious about.

**Gates.**
- The first sentence carries the thesis or its sharpest consequence — unless a withheld-reveal structure has been chosen under `NAR-03` or `OPN-01`, in which case the first sentence states the map instead of the answer, and the choice is written down.
- The counter-intuitive element is identified and stated, not left implicit.
- Any central metaphor has been tested on an unbriefed case.

**Failure signals.**
- Your best line is in the last paragraph.
- You are proud of how much you fitted in.
- You plan to say it ten times *within one piece*. If it needs ten tellings in one sitting, the idea is badly designed. Repetition **across** forms and occasions is a different thing and is required — see `CMP-01` and `ACT-03`.
- The metaphor is a handshake over a globe, a rocket, a journey with no destination, or a machine with people as parts.

---

## MSG-03 — Pyramid discipline

**Trigger.** Any document, memo, deck, or argument that must be followed rather than felt.

**Procedure.**

1. Build a pyramid under the thesis. Ideas relate **vertically** (each point summarizes the ideas grouped below it, creating a question-and-answer dialogue with the reader) and **horizontally** (ideas sit together because together they make one argument).
2. Think bottom-up — that is how ideas are actually developed — and present top-down where the audience wants the answer and already extends you enough trust to accept it. Where trust has to be built first, or the audience cares how you got there, chronological order is the right choice instead; see `DAT-04`. Say which one you are doing.
3. Run the three rules on the outline **before writing a sentence**:
   - Ideas at any level must be **summaries** of the ideas grouped below them.
   - Ideas in each grouping must be the **same kind** of idea — nameable by one plural noun (reasons, steps, risks, changes).
   - Ideas in each grouping must be **logically ordered**.
   A broken rule is a bug report on the thinking, not a formatting nit.
4. Choose the order from the analysis that produced the grouping: cause-and-effect → time order; dividing a whole into parts → structural order; classifying like things → order of importance. If no order can be found, the grouping is invalid or incomplete. Fix it; do not ship it.
5. Divide **MECE** — mutually exclusive, collectively exhaustive — and state the principle of division.
6. Prefer **induction** at the top level and push deduction as low as possible; deduction costs the audience more effort. Cap a deductive chain at about four points and two chained "therefores". Never mix the two in one grouping.
7. Word every action as an **end product**: visualize a real person doing it and name what they are holding when it is done. "Assign planning responsibility to the regions" — not "strengthen regional effectiveness". If you cannot picture the end product, you cannot tell whether a step is missing.
8. Open with the reminder structure: a **Situation** the audience already accepts → the **Complication** that disturbs it → the **Question** it raises → the **Answer**, which is your thesis. Include nothing in the opening the audience does not already accept as true; new information there distorts the question they think they are being asked.

**Gates.**
- All three pyramid rules pass on the outline.
- Every grouping has a findable order and a plural-noun label.
- Every action is stated as an end product.
- The opening contains no new information.

**Failure signals.**
- A list where you cannot say why the second point comes second.
- A point that refers to all the other points — it belongs above them, not beside them.
- "Improve", "strengthen", "review", "leverage", "tackle" — no end product; unfixable until reworded.
- A "Background" or "Our Assumptions" section before the message.
- Groupings past five points with no subgrouping.

---

## MSG-04 — Structure selection

**Trigger.** After the thesis exists and the material has been gathered.

**Procedure.** Choose deliberately; message order alone motivates or demotivates.

| Situation | Structure |
|---|---|
| The audience already feels the pain | problem → solution |
| Two rival options are live | compare / contrast |
| Diagnosing a failure | cause → effect |
| A trade-off must be weighed | advantage / disadvantage |
| The audience needs momentum or history | chronological |
| Teaching a method | sequential |
| Describing a system or a place | spatial |
| Building to a decision or a reveal | climactic |
| Contested case, formal setting | exposition → narrative → division → evidence → **refutation** → summary |
| Advocacy that must end in action | attention → problem → solution → **visualization** → call to action |
| Persuasion by contrast | what is → the gap → what could be, oscillating → the ask → the new state |
| The audience only needs a taxonomy | topical (least engaging; use sparingly) |

Notes that matter more than the table:

- The **refutation** step is what buys quasi-judicial credibility. A structure without it reads as advocacy, which is what a skeptical audience discounts.
- The **visualization** step — letting them see success concretely — is the most moving step in the advocacy sequence and the one most often skipped.
- The **contrast** structure is an engine, not a decoration: an idea juxtaposed with its opposite creates the tension the rest of the piece resolves. That means you need real material on **both** sides. A thin "what is" makes the proposal feel unearned.
- Never lead with "what could be". Establish the audience's current reality first, in their own terms, so they nod before you ask them to move.
- Never announce the structure as though it were the content. A road-map sentence is fine; a slide about your agenda is not the message.

**Gates.**
- The chosen structure is named, together with the structure considered and rejected.
- Refutation is present in any contested case.
- Both sides of any contrast are populated.

**Failure signals.**
- The structure is "everything I know, in the order I learned it".
- Five minutes of problem in a seven-minute talk.
- A solution announced and then immediately applauded, with no persuasion in between.

---

## MSG-05 — Beats, sections, and the section brief

**Trigger.** Once the structure is chosen and before drafting.

**Procedure.**

1. Break the piece into **thought modules**: one idea plus everything needed to support it. Modules nest; the whole piece is one module whose idea is the thesis.
2. For each section, write a one-line brief:

   ```
   purpose:              (what this section is for)
   key claim:
   logical function:     (what it proves or establishes)
   emotional function:   (what the audience should feel by the end of it)
   evidence:             (which specific item)
   carried by:           (language / story / wit / support — at least one)
   transition out:
   expected reaction:
   ```

3. Audit the **beats**: analytical and emotional content must alternate. Do not enthymematize continuously — a run of pure argument fatigues an audience regardless of its quality. Interleave proof with character and feeling.
4. Any section carrying none of language, story, wit or support is where the audience disengages. Fix it or cut it.
5. Pare hard. List far more candidate points than you need, then cut to **three or four** (five maximum) for a twenty-to-thirty-minute piece. Selection test: *if I could tell this audience only three things, what would they be?*
6. Plot the **few lines that must land** first, and accept that the rest is connective tissue whose job is to make those lines stand out. A major speech is a small fraction of load-bearing content; deliberately leaving passages flat is what gives the peaks somewhere to rise from.
7. Write a **mini-opening** (situation, complication, question) at the head of each major section of a long piece, written from where the audience now stands.

**Gates.**
- Every section has a purpose, a claim, and at least one of language / story / wit / support.
- Analytical and emotional beats alternate.
- The point count is 3–5, not 12.
- The lines that must land are identified before drafting.

**Failure signals.**
- Every section is analytical.
- A section you cannot state the purpose of.
- Twelve points, each mentioned once.
- Transitions that only say "and now, moving on to".

---

## Defaults and thresholds

| Decision | Default |
|---|---|
| Thesis length | one sentence; a talk's throughline ≤ 15 words |
| Key points, 20–30 minute piece | 3–4, absolute maximum 5 |
| Candidate points to generate first | 15–20, then cut |
| Grouping size | 3–5; subgroup beyond that |
| Deductive chain | ≤ 4 points, ≤ 2 chained "therefores" |
| Opening comprehension window | the whole argument in ~30 seconds |
| Content volume vs. slot | build for ~60% of the slot |
| Load-bearing lines in a major speech | a handful; the rest is scaffolding |

---

## Related

`AUD-01` supplies the objective this thesis serves. `NAR-01` supplies the story spine when the structure is narrative. `LOG-03` orders the proofs inside the structure. `OPN-01` writes the opening this module specifies. `VIS-01` converts sections into slides — never the reverse. `REV-01` re-tests the pyramid rules after editing.
