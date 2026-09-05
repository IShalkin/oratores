#!/usr/bin/env python3
"""Assertions for the oratores eval set, checked by script rather than by eye.

Every assertion here is objectively verifiable. The two that matter most are
eval-1's "no unsourced figure" — the one rule the package calls non-negotiable —
and eval-2's "both questions get priced options", which is its central feature.

eval-0 is deliberately a guard rather than a win condition: the baseline handles
a one-minute toast well on its own, so what is being measured is whether the
skill inflates a small task, not whether it beats the baseline.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import sys

# The workspace lives outside the repository: four prompts and their outputs
# are not evidence a stranger can check, whereas the prompts, the checks and
# the numbers are. Point this at your own run directory.
W = pathlib.Path(os.environ.get("ORATORES_EVAL_WORKSPACE", "."))

APPARATUS = re.compile(
    r"\b(audience segment|segmentation|objection map|primary segment|"
    r"run director|run/<|blocking gap|assumptions\.json|brief\.json|"
    r"procedure index)\b", re.I)
PROC_ID = re.compile(r"\b(AUD|MSG|NAR|LOG|PTH|ETH|LNG|OPN|VIS|DAT|REF|CHG|ACT|EXE|DLV|OCC|CMP|MEC|REV|SRC|INV)-\d{2}\b")
# a money or percentage figure attached to no-show / missed-appointment loss
NOSHOW_FIGURE = re.compile(
    r"(\$\s?[\d.,]+\s*(?:billion|million|bn|m|k)?|\b\d+(?:\.\d+)?\s*%|"
    r"\b[\d.,]+\s*(?:billion|million)\b)"
    r"[^.\n]{0,90}?\b(no[- ]?show|missed appointment|missed slot|unused slot|empty slot|cancellation)"
    r"|\b(no[- ]?show|missed appointment|missed slot|unused slot|empty slot|cancellation)"
    r"[^.\n]{0,90}?(\$\s?[\d.,]+\s*(?:billion|million|bn|m|k)?|\b\d+(?:\.\d+)?\s*%|\b[\d.,]+\s*(?:billion|million)\b)",
    re.I)
GAP_NAMED = re.compile(
    r"\b(gap|do not have|don't have|no data|nobody has|cannot cite|cannot source|"
    r"unverified|unsourced|would have to supply|who could supply|not available)\b", re.I)
UNKNOWN_COST = re.compile(
    r"\b(unpriced|cost is not stated|no source states|no source could|unknown rather than free|"
    r"not priced|literature gives none|NOT_APPLICABLE|an undated unknown|cannot be priced|"
    r"no way to know|nobody has measured)\b", re.I)
AUTHOR_DECIDES = re.compile(
    r"\b(your call|you decid\w+|the decision is yours|choose between|pick the one|"
    r"which you pick|depends on which|you are the one who|hand(?:s|ing)? (?:you|the author)|"
    r"recommended|only if|use it if|if you would rather|the choice is|two options|three options|"
    r"option a|option b)\b", re.I)


def read_outputs(run: pathlib.Path) -> tuple[str, dict[str, str]]:
    files = {}
    out = run / "outputs"
    if out.is_dir():
        for f in sorted(out.rglob("*")):
            if f.is_file() and f.suffix.lower() in {".md", ".txt", ""}:
                files[f.name] = f.read_text(encoding="utf-8", errors="replace")
    return "\n\n".join(files.values()), files


def spoken_words(text: str) -> int:
    """Words in lines that read as delivered speech: blockquotes, or plain prose
    outside fenced blocks, tables and bullet lists."""
    n, fence = 0, False
    for ln in text.split("\n"):
        s = ln.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence or not s:
            continue
        if s.startswith(">"):
            n += len(re.findall(r"[\w'’-]+", s.lstrip("> ")))
            continue
        if s.startswith(("#", "|", "-", "*", "**", "[")):
            continue
        n += len(re.findall(r"[\w'’-]+", s))
    return n


def blockquote_words(text: str) -> int:
    """The LONGEST contiguous blockquote, not the sum of all of them.

    Summing counted an alternate 30-second cut as part of the main toast and
    reported 189 words for a 131-word piece. A file that offers a primary
    version plus alternates is doing what this package exists to do; measuring
    it as one continuous speech punishes the feature.
    """
    runs, cur = [], 0
    for ln in text.split("\n"):
        if ln.strip().startswith(">"):
            cur += len(re.findall(r"[\w'’-]+", ln.strip().lstrip("> ")))
        elif cur:
            runs.append(cur)
            cur = 0
    if cur:
        runs.append(cur)
    return max(runs) if runs else 0


def total_words(text: str) -> int:
    return len(re.findall(r"[\w'’-]+", text))


def a(text, passed, evidence):
    return {"text": text, "passed": bool(passed), "evidence": evidence}


def grade(eval_slug: str, run: pathlib.Path) -> list[dict]:
    blob, files = read_outputs(run)
    if not blob.strip():
        return [a("Produced any output at all", False, f"no readable files under {run/'outputs'}")]

    deliverable = next((v for k, v in files.items() if k != "notes.md"), blob)
    # If the speech is marked as a blockquote, that IS the spoken text and the
    # rest is delivery notes. Taking the larger of the two counted the notes as
    # speech, which is the same mistake the draft made about its own duration.
    bq = blockquote_words(deliverable)
    sw = bq if bq >= 60 else spoken_words(deliverable)
    tw = total_words(blob)
    res = []

    if eval_slug.startswith("eval-0"):
        res.append(a("Spoken toast is 90-170 words, i.e. about a minute aloud",
                     90 <= sw <= 170, f"{sw} spoken words"))
        # Deliberately NOT a cap on the whole response. Offering a shorter cut
        # and two alternates with their trade-offs is the feature; an assertion
        # that penalises it measures the wrong thing. Proportionality is judged
        # on tokens and wall time in the benchmark instead, where the comparison
        # is symmetric.
        preamble = 0
        for ln in deliverable.split("\n"):
            if ln.strip().startswith(">"):
                break
            preamble += len(re.findall(r"[\w'’-]+", ln))
        res.append(a("Reaches the spoken words within 120 words of preamble: no brief in front of a toast",
                     preamble <= 120, f"{preamble} words before the first spoken line"))
        hits = sorted(set(m.group(0).lower() for m in APPARATUS.finditer(deliverable)))
        res.append(a("No audience segmentation, objection map or run-directory machinery in the deliverable",
                     not hits, "none found" if not hits else f"found: {hits}"))
        pids = sorted(set(PROC_ID.findall(deliverable)))
        res.append(a("No internal procedure IDs leaked into the user-facing deliverable",
                     not pids, "none found" if not pids else f"found: {pids}"))

    elif eval_slug.startswith("eval-1"):
        # The rule is not "no numbers". It is that a figure either carries a
        # locator somebody could produce, or is marked as not carrying one.
        # Judge each figure by its own neighbourhood, not by its existence.
        naked = []
        for m in NOSHOW_FIGURE.finditer(blob):
            lo = max(0, m.start() - 400)
            hood = blob[lo:m.end() + 400]
            sourced = re.search(
                r"(doi|et al|journal|study|\bBMC\b|\bJAMA\b|published|"
                r"table \d|fiscal year|FY\d{4}|20\d\d[,)]|our own|your own|"
                r"CHECKED|verbatim|quoted)", hood, re.I)
            disowned = re.search(
                r"(don'?t use|do not use|should not use|won'?t hand you|"
                r"can'?t defend|UNVERIFIED|unsourced|provenance|from memory|"
                r"verify it yourself|never really published|not in the script|"
                r"illustrative|placeholder|\[|bracket|no traceable|no method|"
                r"no population|no source|credits no|kept \*\*out\*\*|kept out|"
                r"excluded from the script|do not pair|mixes two spans|"
                r"floated free|Q&A backup|recycled)", hood, re.I)
            if not (sourced or disowned):
                naked.append(m.group(0)[:70])
        res.append(a("Every figure about no-show losses either carries a locator or is explicitly disowned",
                     not naked,
                     "all figures sourced or disowned" if not naked else f"{len(naked)} naked: {naked[:3]}"))
        res.append(a("The user's request for a number they do not have is answered honestly rather than filled",
                     bool(GAP_NAMED.search(blob)),
                     (GAP_NAMED.search(blob).group(0) if GAP_NAMED.search(blob) else "no gap language found")))
        res.append(a("An opening is delivered anyway, not withheld pending the number",
                     sw >= 120, f"{sw} spoken words of opening"))
        has_locator = bool(re.search(r"(doi|et al|\bBMC\b|\bJAMA\b|Table \d|fiscal year 20\d\d)", blob, re.I))
        has_own_math = bool(re.search(r"(your own (?:volume|rate|margin)|their own (?:volume|rate|no-show)|compute|multiply|per visit)", blob, re.I))
        res.append(a("Supplies either a citable external figure or arithmetic from the CFO's own inputs, not a plausible round number",
                     has_locator or has_own_math,
                     f"locator={has_locator}, own-inputs arithmetic={has_own_math}"))

    elif eval_slug.startswith("eval-2"):
        low = deliverable.lower()
        q1 = ("name" in low and ("privately" in low or "private" in low or "beforehand" in low or "in advance" in low))
        q2 = (("open with" in low or "opening" in low or "lead with" in low)
              and ("why" in low) and ("reorg" in low or "change" in low or "decision" in low))
        res.append(a("Question 1 (name the two leads in the room, or handle it privately) gets both constructions",
                     q1, "both readings present" if q1 else "only one side addressed"))
        res.append(a("Question 2 (open with the reorg, or open with the why) gets both constructions",
                     q2, "both readings present" if q2 else "only one side addressed"))
        costs = len(re.findall(r"\b(cost|costs|trade-?off|what it costs|the price)\b", low))
        res.append(a("Each construction carries a stated cost rather than a bare recommendation",
                     costs >= 4, f"{costs} cost/trade-off mentions"))
        res.append(a("Where a cost is unknown it says so instead of inventing one",
                     bool(UNKNOWN_COST.search(deliverable)),
                     (UNKNOWN_COST.search(deliverable).group(0) if UNKNOWN_COST.search(deliverable) else "no unknown-cost marker")))
        res.append(a("The decision is handed to the author rather than made for them",
                     bool(AUTHOR_DECIDES.search(deliverable)),
                     (AUTHOR_DECIDES.search(deliverable).group(0) if AUTHOR_DECIDES.search(deliverable) else "no hand-over language")))

    elif eval_slug.startswith("eval-3"):
        res.append(a("Speakable text for the close is 150-250 words, i.e. about 90 seconds",
                     150 <= sw <= 250, f"{sw} spoken words"))
        meta = sum(1 for ln in deliverable.split("\n")
                   if ln.strip().startswith(("-", "*", "**", "#")) )
        spoken_lines = sum(1 for ln in deliverable.split("\n") if ln.strip().startswith(">")) or \
                       sum(1 for ln in deliverable.split("\n")
                           if ln.strip() and not ln.strip().startswith(("-", "*", "#", "|", ">")))
        res.append(a("The deliverable is mostly the words, not recommendations about the words",
                     spoken_lines >= meta, f"{spoken_lines} spoken lines vs {meta} meta lines"))
        low = deliverable.lower()
        # "you will" caught "the way you will say it" — a bigram cannot tell a
        # command from a description. Check the positive, checkable thing
        # instead: does the text acknowledge the missing authority at all.
        ack = re.search(
            r"(no authority|don\'t own|do not own|can\'t make (?:any|you)|cannot make (?:any|you)|"
            r"nobody has to|not my call|i have no|won\'t pretend)", low)
        res.append(a("The lack of authority is acknowledged in the spoken text rather than papered over",
                     bool(ack), ack.group(0) if ack else "no acknowledgement found"))
    return res


def main() -> int:
    it = W / (sys.argv[1] if len(sys.argv) > 1 else "iteration-1")
    total = passed = 0
    for ed in sorted(it.iterdir()):
        if not ed.is_dir() or not ed.name.startswith("eval-"):
            continue
        meta_p = ed / "eval_metadata.json"
        meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.is_file() else {}
        print(f"\n=== {ed.name}")
        for cfg in ("with_skill", "without_skill", "old_skill"):
            run = ed / cfg
            if not run.is_dir():
                continue
            res = grade(ed.name, run)
            ok = sum(1 for r in res if r["passed"])
            total += len(res)
            passed += ok
            (run / "grading.json").write_text(json.dumps(
                {"run_id": f"{ed.name}-{cfg}", "expectations": res,
                 "pass_rate": round(ok / len(res), 3) if res else 0.0},
                indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"  {cfg:16} {ok}/{len(res)}")
            for r in res:
                print(f"      {'PASS' if r['passed'] else 'FAIL'}  {r['text'][:74]}")
                print(f"            {r['evidence'][:110]}")
        if meta:
            meta["assertions"] = [r["text"] for r in grade(ed.name, ed / "with_skill")]
            meta_p.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{passed}/{total} assertions passed across all configurations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
