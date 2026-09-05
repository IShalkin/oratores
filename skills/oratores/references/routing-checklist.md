# Routing Checklist — maintainers only

**Never load this during a user task.** It is a checklist for editing this skill, not for using it. Loading it while drafting for a user wastes context and produces meta-commentary instead of a deliverable.

---

## Before adding a procedure

1. Does an existing procedure already cover it? Extend that one. A near-duplicate procedure is worse than a long one, because routing then depends on a distinction nobody can state.
2. Is it a **procedure** (a repeatable sequence with gates) or a **fact** (something true about persuasion)? Facts belong inside an existing procedure's body. Only sequences get IDs.
3. Does it have all four sections — Trigger, Procedure, Gates, Failure signals? A procedure with no failure signals has not been thought through; the failure signals are what make it diagnosable in review.
4. Are the Gates checkable by someone who did not write them? "Consider the audience" is not a gate. "One primary segment is chosen and stated" is.
5. Add the row to `procedure-index.md`, and add it to the module map count.

## Before adding a module

1. Would the procedures fit in an existing module? Twenty-one modules is already past the edge of what a router can comfortably select from.
2. Add it to: the Task Router in `SKILL.md`, the Context Loading Protocol if it is boundary-triggered, `procedure-index.md` (rows plus module map), and the Related sections of every module it interacts with.
3. Pick a three-letter prefix that is not already used and is not confusable with one that is.

## Before adding a boundary

The Context Loading Protocol boundary list is deliberately capped at ten. A boundary earns a place only if:

1. A request would **routinely fail to mention it**. A boundary the user always states is not a boundary; it is an input.
2. Missing it produces a materially wrong deliverable, not merely a thinner one.
3. It maps to a specific procedure that would otherwise not be loaded.

Adding an eleventh means removing one. Say which, and why, in the commit.

## Before adding a playbook

See `playbooks/README.md`. The one failure mode to watch: a playbook that restates module content instead of routing to it. If the general module lacks what the genre needs, **add it to the module** — otherwise every future genre has to rediscover it.

## Consistency checks

Run these by hand when editing; `scripts/validate_skill.py` checks the mechanical ones.

- Every procedure ID referenced anywhere exists in `procedure-index.md`.
- Every ID in `procedure-index.md` appears as a `## <ID> — ` heading in its named file.
- Every relative link resolves.
- Every module named in the `SKILL.md` Task Router exists.
- Every fork skill's links into `../oratores/references/` resolve.
- The module map counts in `procedure-index.md` match the actual heading counts.
- Boundary count in `SKILL.md` is ten, and every boundary has a mapped procedure in the index.

## What this package does not enforce

Everything here is text a model reads, and text can be declined. Two things only are enforced mechanically:

1. **The critic agent's tool grant.** `oratores-critic` has no Write, no Edit and no Bash, so it cannot alter what it reviews. A tool never granted is a mechanism; a filter over commands is best-effort.
2. **The validators**, which check structure, addressing and countability.

In particular, the review-debt rule, the module budget, the boundary pass and the seven-question cap are **conventions the model follows, not gates that stop it**. Read a green validator run as "the package is structurally intact", never as "the guidance was applied".

There is a third thing worth stating plainly, because it is the honest limit of a package like this: nothing here can verify that a claim in a delivered piece was true, that a cited peer really adopted, or that a stated limit was real. Those are properties of the world, checked by people. The package can require that they be checked, and it cannot check them.

## Corpus maintenance

`docs/sources.md` records the corpus this synthesis was built from. When adding to it:

- Record the specific edition or translation, because both change the content materially.
- Record the known defect if the source had one — a partial scan, a non-English edition, a revised framework — because a synthesis built on a defective source inherits the defect silently.
- Do **not** add a source to the list without folding its distinct contribution into a module. A bibliography that is longer than the synthesis is a citation, not a source.
