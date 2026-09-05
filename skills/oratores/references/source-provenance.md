# Source and Provenance — SRC

Attribution discipline. Two procedures, both narrow, both frequently the difference between a credible piece and an embarrassing one.

---

## SRC-01 — Named-source claims

**Trigger.** The piece attributes something to a named author, book, speech, study, company, or case. Also whenever the user asks "what does X say about Y".

**Procedure.**

1. Decide which kind of claim you are making, because the requirement differs:

   | Claim | Requires |
   |---|---|
   | "This is the general shape of the argument" | nothing beyond ordinary care; state it as synthesis |
   | "X argues that…" | the position, correctly attributed, and confidence that it is X's own position |
   | "X says: '<quotation>'" | the source artifact, and a locator — chapter, section, page, or line |
   | "The study found N%" | the study, its population, its date, and what it measured |
   | "Company C achieved R" | the published account, and whether R is theirs or a vendor's claim |

2. If a source pack for that author or work is installed alongside this skill, read it before answering. It exists for exactly this: deeper rationale, exact wording, and the uncommon variants that a synthesis compresses away.
3. If no source is available, choose one and say which:
   - restate the claim as **synthesis** — "the standard view is…", "practitioners generally hold…" — and do not attribute it to a person; or
   - keep its type and set its source status to `UNVERIFIED`, with the reason, and say what would verify it.
   **Do not substitute a plausible reconstruction for a citation.** A quotation assembled from memory is the failure mode this procedure exists to prevent, and it is unrecoverable once found.
4. Emit the status when the response is source-routed:
   ```
   source_pack_status: loaded:<pack> | unavailable:<artifact> | insufficient_identity:<what is missing> | not_applicable
   ```
   Only source-routed responses need this. Do not attach it to ordinary drafting.
5. Watch the specific hazards that produce most misattribution:
   - **Dialogue and reported speech.** A position voiced by a character in a dialogue is not necessarily the author's. Check the attribution before citing.
   - **Translation.** Wording differs, sometimes materially, between translations of the same text. Do not blend two translations into one quotation, and name the translation when the wording is the point.
   - **Edition.** Frameworks change between editions — a principle added, a chapter revised, a figure updated. Name the edition where it matters.
   - **The famous misattribution.** A line everyone knows is more likely than average to be attributed to the wrong person. Treat familiarity as a reason to check, not a reason not to.
   - **The secondary summary.** A widely repeated summary of a book is often subtly wrong in the same way everywhere, because everyone copied the same source.
6. In the delivered piece, attribute **in the sentence** rather than in a footnote nobody hears. Attribution is cheap; make it. And keep the standard high on wording: a distinctive phrase needs credit even where a paraphrase would not.
7. Reuse of an **idea** through substantial paraphrase is normal practice and needs no apology. Reuse of **wording** needs credit.

**Gates.**
- Every quotation has a locator, or is not presented as a quotation.
- Every statistic has its source, population and date, or carries the source status `UNVERIFIED` with its reason.
- No reconstruction presented as a citation.
- Dialogue, translation and edition hazards checked where they apply.

**Failure signals.**
- "As someone once said…"
- "I believe it was X who said…"
- A quotation with the author's name and no work.
- A figure attributed to a body rather than to a document.
- A famous line attributed confidently and incorrectly.

---

## SRC-02 — Version-sensitive and current claims

**Trigger.** The claim depends on something that changes: a regulation, a market position, a capability, a price, a headcount, a competitive fact, an organizational structure, or the state of a technology.

**Procedure.**

1. Identify what could have changed since you learned it, and when you learned it.
2. Verify against the primary source — the regulation itself, the filing, the published documentation, the person who owns the number. A secondary account of a current fact is a historical account of it.
3. Where verification is not available, set the claim's source status to `UNVERIFIED` with its reason, use the conservative version, and make the verification an explicit open item with an owner. The claim keeps its type — a claim of fact nobody has checked is still a claim of fact, and demoting the type hides which of the two things is missing. Do not quietly use the confident version.
4. Date the claim in the piece where the date matters: "as of last quarter", "under the rules as they stand today". This is not hedging; it is the difference between a defensible statement and a hostage.
5. Where a regulatory or legal position is genuinely unsettled, say it is unsettled and say what you are doing in the meantime. "The rules are not settled, so here is the boundary we are working inside" is a stronger position than either confidence or silence.
6. Re-verify before every re-delivery of a repeated piece. A claim that was `CHECKED` and whose underlying fact has since moved is `RECHECK`, and only checking it again returns it to `CHECKED`. A stock talk carries stale facts forward, and the person who catches one is the person you most needed to convince.

**Gates.**
- Every changeable claim carries a source status, and one checked before the thing it depends on moved is `RECHECK`.
- The conservative version is used where verification failed.
- Dates attached where they matter.
- Repeated pieces re-verified before re-delivery.

**Failure signals.**
- A market-position claim with no date.
- A capability described in the present tense that was true at a demo eight months ago.
- A regulatory statement delivered with more confidence than the regulator has.
- A signature talk on its tenth delivery with its original numbers.

---

## Related

`LOG-04` supplies the claim types and the source statuses this module enforces. `LNG-05` handles the craft of quotation. `MEC-03` handles the case where the verified version is weaker than the one you wanted. `REV-01` pass 4 is where verification actually happens. The corpus this synthesis was built from is recorded in `docs/sources.md` in the source repository.
