#!/usr/bin/env python3
"""Structural validator for the oratores skill package.

Checks the mechanical properties only: structure, addressing, countability.
A green run means the package is structurally intact. It says nothing about
whether the guidance is good or whether it was followed.

Run from anywhere:
    python skills/oratores/scripts/validate_skill.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT = Path(__file__).resolve()
SKILL_DIR = SCRIPT.parent.parent                      # skills/oratores
SKILLS_ROOT = SKILL_DIR.parent                        # skills
REPO = SKILLS_ROOT.parent                             # repo root
REFS = SKILL_DIR / "references"

# Expected prefix -> (module filename, procedure count)
MODULES: dict[str, tuple[str, int]] = {
    "AUD": ("audience-and-intent.md", 5),
    "MSG": ("message-architecture.md", 5),
    "INV": ("invention.md", 5),
    "NAR": ("narrative-and-story.md", 4),
    "LOG": ("evidence-and-logos.md", 5),
    "PTH": ("emotion-and-pathos.md", 5),
    "ETH": ("credibility-and-ethos.md", 4),
    "LNG": ("language-and-figures.md", 5),
    "OPN": ("openings-and-closings.md", 3),
    "VIS": ("slides-and-visuals.md", 4),
    "DAT": ("data-storytelling.md", 4),
    "REF": ("objection-and-refutation.md", 4),
    "CHG": ("belief-change-and-adoption.md", 5),
    "ACT": ("organizational-activation.md", 5),
    "EXE": ("executive-persuasion.md", 4),
    "DLV": ("delivery-and-rehearsal.md", 5),
    "OCC": ("occasion-and-genre.md", 3),
    "CMP": ("campaign-and-cadence.md", 3),
    "MEC": ("mechanism-and-exposure.md", 5),
    "REV": ("revision-and-review.md", 4),
    "SRC": ("source-provenance.md", 2),
}

FORK_SKILLS = [
    "speech-draft",
    "deck-build",
    "audience-strategy",
    "persuasion-audit",
    "exec-activation",
]

AGENTS = [
    "oratores.md",
    "oratores-strategist.md",
    "oratores-evidence.md",
    "oratores-adversary.md",
    "oratores-invention.md",
    "oratores-critic.md",
]

# The ownership table in agents/oratores.md is the single source of truth for
# who holds which part of the corpus.
OWNERSHIP_ROW_RE = re.compile(
    r"^\|\s*(?:\*\*)?(you|`oratores-[a-z]+`)(?:\*\*)?\s*\|([^|]*)\|",
    re.MULTILINE,
)

ID_RE = re.compile(r"\b([A-Z]{3})-(\d{2})\b")
HEADING_ID_RE = re.compile(r"^##\s+([A-Z]{3}-\d{2})\s+—", re.MULTILINE)
INDEX_ROW_RE = re.compile(r"^\|\s*([A-Z]{3}-\d{2})\s*\|", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)

errors: list[str] = []
warnings: list[str] = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO)).replace("\\", "/")
    except ValueError:
        return str(path)


def check_layout() -> None:
    required = [
        REPO / "README.md",
        REPO / "LICENSE",
        SKILL_DIR / "SKILL.md",
        REFS / "procedure-index.md",
        REFS / "routing-checklist.md",
        REFS / "playbooks" / "README.md",
    ]
    for name in AGENTS:
        required.append(REPO / "agents" / name)
    for fork in FORK_SKILLS:
        required.append(SKILLS_ROOT / fork / "SKILL.md")
    for _, (fname, _) in MODULES.items():
        required.append(REFS / fname)

    for path in required:
        if not path.is_file():
            errors.append(f"missing required file: {rel(path)}")


def check_frontmatter() -> None:
    targets = [SKILL_DIR / "SKILL.md"]
    targets += [SKILLS_ROOT / f / "SKILL.md" for f in FORK_SKILLS]
    targets += [REPO / "agents" / a for a in AGENTS]

    for path in targets:
        if not path.is_file():
            continue
        text = read(path)
        m = FRONTMATTER_RE.match(text)
        if not m:
            errors.append(f"{rel(path)}: missing YAML frontmatter")
            continue
        fm = m.group(1)
        if not re.search(r"^name:\s*\S", fm, re.MULTILINE):
            errors.append(f"{rel(path)}: frontmatter has no name")
        if not re.search(r"^description:\s*\S", fm, re.MULTILINE):
            errors.append(f"{rel(path)}: frontmatter has no description")
        # name must match the directory or filename
        name_m = re.search(r"^name:\s*(\S+)", fm, re.MULTILINE)
        if name_m:
            declared = name_m.group(1).strip().strip('"').strip("'")
            expected = path.parent.name if path.name == "SKILL.md" else path.stem
            if declared != expected:
                errors.append(
                    f"{rel(path)}: frontmatter name '{declared}' "
                    f"does not match '{expected}'"
                )


def check_procedure_headings() -> None:
    """Every module has exactly the expected procedure headings, numbered from 01."""
    for prefix, (fname, count) in MODULES.items():
        path = REFS / fname
        if not path.is_file():
            continue
        found = HEADING_ID_RE.findall(read(path))
        expected = [f"{prefix}-{i:02d}" for i in range(1, count + 1)]
        if found != expected:
            errors.append(
                f"{rel(path)}: procedure headings {found or '[]'} "
                f"!= expected {expected}"
            )


def check_index_coverage() -> tuple[set[str], set[str]]:
    """Index rows and module headings must be the same set."""
    index_path = REFS / "procedure-index.md"
    if not index_path.is_file():
        return set(), set()

    index_ids = set(INDEX_ROW_RE.findall(read(index_path)))

    heading_ids: set[str] = set()
    for _, (fname, _) in MODULES.items():
        path = REFS / fname
        if path.is_file():
            heading_ids.update(HEADING_ID_RE.findall(read(path)))

    for pid in sorted(index_ids - heading_ids):
        errors.append(f"procedure-index.md lists {pid} with no matching module heading")
    for pid in sorted(heading_ids - index_ids):
        errors.append(f"{pid} is defined in a module but absent from procedure-index.md")

    return index_ids, heading_ids


def check_referenced_ids(known: set[str]) -> None:
    """Any ID mentioned anywhere in the package must be defined."""
    scan: list[Path] = [SKILL_DIR / "SKILL.md"]
    scan += sorted(REFS.rglob("*.md"))
    scan += [SKILLS_ROOT / f / "SKILL.md" for f in FORK_SKILLS]
    scan += [REPO / "agents" / a for a in AGENTS]
    scan += sorted((REPO / "docs").glob("*.md"))

    for path in scan:
        if not path.is_file():
            continue
        for prefix, num in ID_RE.findall(read(path)):
            if prefix not in MODULES:
                continue
            pid = f"{prefix}-{num}"
            if pid not in known:
                errors.append(f"{rel(path)}: references undefined procedure {pid}")


def check_module_map_counts() -> None:
    """The module map table in the index must state the real counts."""
    index_path = REFS / "procedure-index.md"
    if not index_path.is_file():
        return
    text = read(index_path)
    total_declared = 0
    for prefix, (fname, count) in MODULES.items():
        row = re.search(
            rf"^\|\s*{prefix}\s*\|\s*{re.escape(fname)}\s*\|\s*(\d+)\s*\|",
            text,
            re.MULTILINE,
        )
        if not row:
            errors.append(f"procedure-index.md: module map has no row for {prefix}")
            continue
        declared = int(row.group(1))
        if declared != count:
            errors.append(
                f"procedure-index.md: module map says {prefix} has {declared} "
                f"procedures; validator expects {count}"
            )
        total_declared += declared

    total_row = re.search(r"\*\*total\*\*\s*\|\s*\*\*(\d+)\*\*", text)
    expected_total = sum(c for _, c in MODULES.values())
    if not total_row:
        errors.append("procedure-index.md: module map has no total row")
    elif int(total_row.group(1)) != expected_total:
        errors.append(
            f"procedure-index.md: module map total says {total_row.group(1)}, "
            f"expected {expected_total}"
        )


def check_boundaries() -> None:
    """SKILL.md declares ten compound boundaries; the index maps all ten."""
    skill = SKILL_DIR / "SKILL.md"
    if skill.is_file():
        text = read(skill)
        block = re.search(
            r"\*\*Compound boundaries\.\*\*(.*?)^## ", text, re.DOTALL | re.MULTILINE
        )
        if not block:
            errors.append("SKILL.md: compound-boundary block not found")
        else:
            items = re.findall(r"^\s*(\d+)\.\s", block.group(1), re.MULTILINE)
            if len(items) != 10:
                errors.append(
                    f"SKILL.md: expected 10 compound boundaries, found {len(items)}"
                )

    index_path = REFS / "procedure-index.md"
    if index_path.is_file():
        text = read(index_path)
        block = re.search(
            r"## Boundary → procedure map(.*?)^## ", text, re.DOTALL | re.MULTILINE
        )
        if not block:
            errors.append("procedure-index.md: boundary map not found")
        else:
            rows = re.findall(r"^\|\s*(\d+)\s+—", block.group(1), re.MULTILINE)
            if sorted(int(r) for r in rows) != list(range(1, 11)):
                errors.append(
                    f"procedure-index.md: boundary map covers {sorted(rows)}, "
                    "expected 1..10"
                )

    check_boundary_parity()


def _ids(text: str) -> set[str]:
    return set(re.findall(r"\b[A-Z]{3}-\d\d\b", text))


def check_boundary_parity() -> None:
    """The SKILL.md boundary list and the index boundary map must agree.

    They drifted once: three boundaries carried an extra procedure in the index
    that SKILL.md did not list, and since the boundary pass is executed from
    SKILL.md those three never loaded from a boundary at all.
    """
    skill = SKILL_DIR / "SKILL.md"
    index_path = REFS / "procedure-index.md"
    if not (skill.is_file() and index_path.is_file()):
        return

    sblock = re.search(
        r"\*\*Compound boundaries\.\*\*(.*?)^## ", read(skill), re.DOTALL | re.MULTILINE
    )
    iblock = re.search(
        r"## Boundary → procedure map(.*?)^## ", read(index_path), re.DOTALL | re.MULTILINE
    )
    if not (sblock and iblock):
        return

    in_skill = {
        int(n): _ids(body)
        for n, body in re.findall(r"^\s*(\d+)\.\s(.*)$", sblock.group(1), re.MULTILINE)
    }
    in_index = {
        int(n): _ids(body)
        for n, body in re.findall(r"^\|\s*(\d+)\s+—(.*)$", iblock.group(1), re.MULTILINE)
    }
    for n in sorted(set(in_skill) | set(in_index)):
        a, b = in_skill.get(n, set()), in_index.get(n, set())
        if a != b:
            errors.append(
                f"boundary {n}: SKILL.md has {sorted(a)}, "
                f"procedure-index.md has {sorted(b)}"
            )


def check_reachability(known: set[str]) -> None:
    """Every indexed procedure must be addressable from SKILL.md.

    A procedure in the index but in no task-router row, no boundary and no
    context-loading step is unreachable: nothing routes to it and it is
    loaded only by accident.
    """
    skill = SKILL_DIR / "SKILL.md"
    if not skill.is_file():
        return
    text = read(skill)
    for pid in sorted(known):
        if pid not in text:
            errors.append(
                f"{pid} is unreachable — it is in procedure-index.md but in no "
                "task-router row, compound boundary or context-loading step"
            )


def check_procedure_sections() -> None:
    """Every procedure carries Trigger, Procedure, Gates and Failure signals.

    A procedure with no gates cannot be failed by the critic; one with no
    failure signals has not been thought through.
    """
    required = ("**Trigger.**", "**Procedure.**", "**Gates.**", "**Failure signals.**")
    for filename, _ in MODULES.values():
        path = REFS / filename
        if not path.is_file():
            continue
        blocks = re.split(r"^## (?=[A-Z]{3}-\d\d)", read(path), flags=re.MULTILINE)[1:]
        for block in blocks:
            pid = block[:6]
            body = re.split(r"^## ", block, flags=re.MULTILINE)[0]
            missing = [s for s in required if s not in body]
            if missing:
                errors.append(
                    f"{filename}: {pid} is missing {', '.join(missing)}"
                )


def check_fork_question_gate() -> None:
    """A forked skill must not instruct the model to ask the caller anything.

    A fork has no return path. A question emitted mid-run does not pause the
    work, it ends it, and the caller sees a stalled agent instead of a
    deliverable. This shipped once and hung a live run.
    """
    for fork in FORK_SKILLS:
        path = SKILLS_ROOT / fork / "SKILL.md"
        if not path.is_file():
            continue
        text = read(path)
        if "cannot ask the caller" not in text:
            errors.append(
                f"{rel(path)}: fork skill must carry the no-questions guard"
            )
        for phrase in ("ask at most seven", "ask at most 7", "ask — at most"):
            if phrase in text:
                errors.append(
                    f"{rel(path)}: fork skill instructs asking questions "
                    f"({phrase!r}); a fork cannot receive an answer"
                )


def check_fork_wiring() -> None:
    """Fork skills must declare fork context and point at the shared references."""
    for fork in FORK_SKILLS:
        path = SKILLS_ROOT / fork / "SKILL.md"
        if not path.is_file():
            continue
        text = read(path)
        fm = FRONTMATTER_RE.match(text)
        fmtext = fm.group(1) if fm else ""
        if "context: fork" not in fmtext:
            errors.append(f"{rel(path)}: fork skill missing 'context: fork'")
        bound = re.search(r"^agent:\s*(\S+)", fmtext, re.MULTILINE)
        if not bound:
            errors.append(f"{rel(path)}: fork skill missing an agent binding")
        elif f"{bound.group(1)}.md" not in AGENTS:
            errors.append(
                f"{rel(path)}: agent binding {bound.group(1)!r} resolves to no "
                f"agent file; known agents are {AGENTS}"
            )
        if "../oratores/references/" not in text:
            errors.append(
                f"{rel(path)}: fork skill does not link into "
                "../oratores/references/"
            )


def check_critic_tool_grant() -> None:
    """The critic's read-only property is a tool grant, not a convention."""
    path = REPO / "agents" / "oratores-critic.md"
    if not path.is_file():
        return
    fm = FRONTMATTER_RE.match(read(path))
    if not fm:
        return
    tools_m = re.search(r"^tools:\s*(.+)$", fm.group(1), re.MULTILINE)
    if not tools_m:
        errors.append(f"{rel(path)}: critic has no explicit tools list")
        return
    granted = {t.strip() for t in tools_m.group(1).split(",")}
    forbidden = granted & {"Write", "Edit", "Bash", "NotebookEdit"}
    if forbidden:
        errors.append(
            f"{rel(path)}: critic must not hold write tools; found {sorted(forbidden)}"
        )
    # `memory:` at any value makes the harness add Read, Write and Edit, which
    # bypasses the allowlist above. Checking `tools:` alone passed this file for
    # most of a day while the grant was actually wide open.
    if re.search(r"^memory:", fm.group(1), re.MULTILINE):
        errors.append(
            f"{rel(path)}: critic declares `memory:`, which auto-enables Write and Edit "
            "and defeats the withheld-tool mechanism; remove the field"
        )


def check_no_maintainer_leak() -> None:
    """The maintainer checklist must not be linked from a user-facing path."""
    for fork in FORK_SKILLS:
        path = SKILLS_ROOT / fork / "SKILL.md"
        if path.is_file() and "routing-checklist" in read(path):
            errors.append(f"{rel(path)}: fork skill must not load routing-checklist.md")
    skill = SKILL_DIR / "SKILL.md"
    if skill.is_file():
        text = read(skill)
        if "routing-checklist" in text and "only while maintaining" not in text:
            warnings.append(
                "SKILL.md links routing-checklist.md without the maintainer-only caveat"
            )


def check_agent_roster() -> None:
    """Every agent in the roster exists, is self-consistent, and can write."""
    for name in AGENTS:
        path = REPO / "agents" / name
        if not path.is_file():
            errors.append(f"agents/{name}: named in the roster but missing")
            continue
        fm = FRONTMATTER_RE.match(read(path))
        if not fm:
            errors.append(f"agents/{name}: no frontmatter")
            continue
        body = fm.group(1)
        declared = re.search(r"^name:\s*(\S+)$", body, re.MULTILINE)
        if not declared or f"{declared.group(1)}.md" != name:
            errors.append(f"agents/{name}: frontmatter name does not match the filename")
        if not re.search(r"^skills:", body, re.MULTILINE):
            errors.append(f"agents/{name}: does not preload the oratores skill")
        if name != "oratores-critic.md":
            tools = re.search(r"^tools:\s*(.+)$", body, re.MULTILINE)
            if not tools or "Write" not in tools.group(1):
                errors.append(f"agents/{name}: a specialist that cannot write its own file")


def check_module_ownership() -> None:
    """No module prefix owned twice, and none left unowned."""
    path = REPO / "agents" / "oratores.md"
    if not path.is_file():
        return
    owner_of: dict[str, str] = {}
    for m in OWNERSHIP_ROW_RE.finditer(read(path)):
        who = m.group(1).strip("`")
        for prefix in re.findall(r"`([A-Z]{3})`", m.group(2)):
            if prefix in owner_of:
                errors.append(
                    f"agents/oratores.md: {prefix} is owned by both "
                    f"{owner_of[prefix]} and {who}"
                )
            owner_of[prefix] = who
    if not owner_of:
        errors.append("agents/oratores.md: no module ownership table found")
        return
    unowned = sorted(set(MODULES) - set(owner_of))
    if unowned:
        errors.append(
            f"agents/oratores.md: no agent owns {', '.join(unowned)} \u2014 "
            "a module nobody owns is a module nobody loads"
        )
    unknown = sorted(set(owner_of) - set(MODULES))
    if unknown:
        errors.append(f"agents/oratores.md: ownership names unknown prefixes {unknown}")
    named = {w for w in owner_of.values() if w != "you"}
    missing = sorted(named - {a[:-3] for a in AGENTS})
    if missing:
        errors.append(f"agents/oratores.md: ownership names agents that do not exist: {missing}")


def check_specialists_write_no_prose() -> None:
    """One agent holds the pen, and no specialist may ask a question it cannot hear."""
    for name in AGENTS:
        if name in ("oratores.md", "oratores-critic.md"):
            continue
        path = REPO / "agents" / name
        if not path.is_file():
            continue
        text = read(path)
        if "Write no prose" not in text:
            errors.append(f"agents/{name}: missing the 'write no prose for the piece' rule")
        if "Do not ask" not in text:
            errors.append(f"agents/{name}: missing the do-not-ask rule; a fork has no return path")


def main() -> int:
    check_layout()
    check_frontmatter()
    check_procedure_headings()
    _, heading_ids = check_index_coverage()
    check_referenced_ids(heading_ids)
    check_reachability(heading_ids)
    check_module_map_counts()
    check_procedure_sections()
    check_boundaries()
    check_fork_wiring()
    check_fork_question_gate()
    check_critic_tool_grant()
    check_no_maintainer_leak()
    check_agent_roster()
    check_module_ownership()
    check_specialists_write_no_prose()

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")

    total = sum(c for _, c in MODULES.values())
    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    print(
        f"OK  {len(MODULES)} modules, {total} procedures, "
        f"{len(FORK_SKILLS)} fork skills, {len(AGENTS)} agents. "
        f"{len(warnings)} warning(s)."
    )
    print("Structure is intact. This says nothing about whether the advice is good.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
