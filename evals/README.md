# Evals

Four test prompts, run twice each — once with the `oratores` skill available, once with no skill at all — and graded by script. `evals.json` holds the prompts, `assertions.py` the checks, `iteration-1-benchmark.json` the result.

The prompts are written the way people actually type: lower case, missing context, an occasion and a deadline and not much else. Each one aims at a claim the package makes about itself rather than at general quality.

| | Tests |
|---|---|
| `tiny-request-stays-tiny` | Proportional execution. A one-minute retirement toast. Does the package inflate a small task? |
| `refuses-to-invent-a-figure` | The one rule the package calls non-negotiable. The user asks for a punchy number and says they have no data. |
| `offers-priced-options` | The central feature. Two genuinely contested constructions in a reorg announcement. |
| `delivers-words-not-a-plan` | The most common failure of this role by the package's own admission. "Write the close." |

## Result, iteration 1

```
                 pass    time      tokens
with_skill      0.938    1103 s   168 840
without_skill   0.887     176 s    41 440
delta          +0.050    +928 s  +127 400
```

Roughly five times the tokens and seven times the wall clock for five points of pass rate. One assertion is marked unreliable in the benchmark and excluded from that reading; on the checks that hold it is 15/15 against 14/15 — a one-assertion gap across four tasks.

An earlier version of this file reported +0.113. That came from a benchmark assembled before the grader's last correction, and it did not survive re-deriving the numbers from a single run of the tool that ships here. The corrected figure is above; the episode is in the benchmark's analyst notes, because a published number that disagrees with the published tool is the defect this package spent a day removing.

## What the pass rate does not show, and why that is the finding

Three of the four with-skill runs dispatched `oratores-critic` on their own draft and acted on its findings **before** writing the file the grader reads. So the assertions measure the post-review output, and the mechanism that produced the difference does not appear in the score at all.

What the critic caught inside those runs, each self-reported:

- **13 findings** on the pitch opening, including two of that run's own regressions — a claim that the script did not say "$150bn" when it did.
- **18 confirmed defects** on the reorg structure. The worst: four claim-ledger rows marked `CHECKED` against a reorganisation plan the agent was never given, in a document that separately listed that plan as evidence still needed.
- **Two invented quantities** in the conference close — "twice the on-call", "a quarter" — in a piece whose own notes asserted there were none.

Two runs reached the same conclusion independently, in their own words, without seeing each other:

> A self-audit sitting next to the text suppresses the check. My notes claimed no invented numbers (there were two), one coined line (four), 176 words (227). **Every error failed in the passing direction.**

> All fail in the **passing** direction: the deliverable looks audited by the thing it names.

That is the measurable value of this package, and it is not "writes better prose". A capable model without the skill already refuses to invent a figure, already offers options with costs, already delivers words when words were asked for — all three baselines did. What it does not do is catch the numbers it invented and then certified as clean in its own notes, because nothing independent looked.

## The instrumentation was wrong more often than the skill was

Four of twelve assertions were wrong on first contact with real output, and all four failed against the skill. Each is documented in `assertions.py` where it was fixed, because the class is more useful than the count:

- Summing every blockquote counted an alternate 30-second cut as part of the main toast — 189 words reported for a 131-word piece.
- A 600-word cap on the whole response penalised the skill for offering priced alternates, which is the feature.
- A `you will` bigram flagged "the way you will say it" as a claim of authority.
- The no-invented-figure check flagged a properly cited *BMC Health Services Research* study with a DOI and a verbatim quoted sentence, and separately flagged a figure quoted expressly in order to warn against using it.

All four are the same shape: **a check that reads one surface and reports a conclusion about the thing.** It is the class the package's own third review named, committed in the tooling built to measure the package.

## Running it

```bash
export ORATORES_EVAL_WORKSPACE=/path/to/your/workspace
python assertions.py                 # grades iteration-1
python assertions.py iteration-2     # a later iteration
```

The workspace holds one directory per eval, each with `with_skill/outputs/` and `without_skill/outputs/`. The grader writes a `grading.json` beside each and prints a summary.

The runs themselves are not in this repository. `run/` is git-ignored, and the eval workspace lives outside it — four prompts and their outputs are not evidence anyone else can check, whereas the prompts, the checks and the numbers are.
