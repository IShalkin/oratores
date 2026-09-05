# Playbooks

A playbook is an **instantiation** of the reference modules for one recurring, high-stakes genre. It defines no new procedures. What it supplies is the three things a general router cannot:

1. **Which procedures run, in what order**, for this genre specifically.
2. **What the finished deliverable contains** — the sections, in sequence, so the output is predictable and reviewable.
3. **The genre's characteristic failure modes**, which are usually not the general ones.

Load a playbook when the request matches its genre. Load it *in addition to* the modules it names, never instead of them: the playbook says what to do and the modules say what makes it correct.

## Available

| Playbook | Genre | Load when |
|---|---|---|
| [exec-ai-adoption.md](exec-ai-adoption.md) | An executive address that must convert a large, senior, sceptical, message-fatigued audience into named commitments, owned pilots, and a cascade through their business units — for AI or any comparable technology adoption | The audience is senior, has heard the subject repeatedly, agrees intellectually, and has not changed behaviour; and the objective is organizational adoption rather than agreement |

## Writing a new playbook

Match the existing shape. A playbook that restates module content instead of routing to it has failed — the content belongs in the module, where every genre can reach it.

```markdown
# <Genre name>

## When this applies / When it does not
## Modules this playbook runs        (table: stage → procedures → what it produces)
## Required inputs                    (and the ≤7 questions; and the defaults if refused)
## The deliverable                    (numbered sections, in output order)
## Genre-specific failure modes        (what goes wrong *here* that the modules don't warn about)
## Quality bar                         (the test that decides whether it is finished)
```

Two rules for the content:

- **Route, do not restate.** If you find yourself explaining how to build an objection map, delete it and point at `REF-01`. If the general module lacks something this genre needs, add it to the module.
- **The quality bar must be falsifiable.** "Is it compelling" is not a bar. A short list of questions an audience member must be able to answer unaided, is.
