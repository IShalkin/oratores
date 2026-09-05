# Brand conformance

Source: **Oratores_UI_Brandbook_v1**, 05.09.2026. Its own page 2 says it is a proposal, not a description of an existing application, and page 24 calls the layouts schematic. This file records what the panel actually does against it.

First, the size of the gap. The brandbook specifies a **product** — five modes, a PACT stepper, an editor with diff and accept/reject, source cards, review debt, export with review status, desktop, tablet, mobile and light theme. This panel is a **read-only view over a run directory** with two write-backs. Most of the brandbook is therefore not implemented because there is nothing here to implement it on, not because it was rejected. The parts that do apply are below.

## Implemented

**Colour, p.6-7.** Both themes, exact hex, as semantic tokens. All seven contrast figures the brandbook states were recomputed and reproduce to the second decimal — `#F2EBDD/#111719` 15.26:1, `#B7C1C3/#1B2427` 8.60:1, `#111719/#8BD4DA` 10.80:1, `#667B80/#1B2427` 3.55:1, `#182126/#FAF7F0` 15.28:1, `#4F6066/#FAF7F0` 6.14:1, `#145C63/#FAF7F0` 7.16:1.

**Tokens, p.22.** Components carry no hex and no ad-hoc spacing. Everything resolves through `--color-*`, `--s-*`, `--radius-*`, `--type-*`, `--motion-*`.

**Type, p.8.** Display 32/40 serif, H1 28/36, H2 22/30, body 16/24, editor 18/30 capped at 72ch, label 14/20, meta 12/18, mono 13/20. Mono is restricted to ids, versions, timestamps and file names — never body text.

**Space and shape, p.10.** Steps 4 through 64, card padding 24, radius 8 controls / 12 cards / 16 dialogs, nav 240. Every control is at least 44 px tall. Focus is 2 px at offset 2. Transitions are 120 ms, and `prefers-reduced-motion` removes them.

**Colour never carries meaning alone, p.6 and p.23.** Agent state renders its word beside the dot. Assumption confidence renders its word beside the coloured edge. Source status renders a symbol and its word. Claim **type** is deliberately not a colour dimension at all — a type says nothing about whether anyone checked the claim, so hue there would encode the wrong axis.

**Brand layer separated from working layer, p.5.** No background architecture, no parallax, no glow, no decorative shadow anywhere in the panel. The mark appears twice and only twice, in the two lockups page 4 prescribes: small in the rail header, large on the empty state. The serif display face is reserved for the wordmark and the empty state; every working surface is sans.

**Voice, p.21.** Section notes are one or two sentences; the longer rationale sits behind a disclosure. Failures say what happened to your input and what to do — "Could not write choices.json. Your selection was not saved."

## Deviations, each deliberate

**Interface language is English.** The brandbook says Russian is primary. The panel renders artifacts the agents write in English, so a Russian chrome would put a seam through every screen. The author chose English for this surface.

**The mark is a raster, where page 4 asks for SVG.** A flat master was supplied on 2026-09-05 and is in use: `mark.png` and `icon.png`, cream field, brass rule, cyan bars, no glow and no shadow. The rail carries the **horizontal lockup** of page 4 — mark left at 34 px, name right in the display face — and the empty state carries the **primary lockup**, mark above the name. `favicon.ico` is cut from the same master. Because it is a raster and not the vector the brandbook specifies, it is used at fixed sizes and never scaled up; the SVG master remains outstanding.

The earlier concept, with the glow page 4 forbids, is kept on the author's disk as `concept-glow.png`. It is not served, not referenced, not used anywhere in the panel, and not published.

One note on its palette: the mark's bars are a more saturated cyan than the `#8BD4DA` action token. That is left alone deliberately — page 4 says not to recolour the mark with semantic colours, so the mark keeps its own cyan and the interface keeps its own.

**Light-theme success and danger are derived, not specified.** The brandbook gives light values for canvas, surface, border, brass and action, and no status colours. `#1F6B3F` and `#9B2C20` were chosen to the criterion the brandbook does state — at least 4.5:1 on canvas — and measure 6.07:1 and 7.07:1.

**A fifth source status.** The brandbook gives four: confirmed, unverified, contradicted, recheck. A projection, an interpretation or an intention has no external source that could confirm it, so forcing those onto *unverified* would make one value mean two unrelated things — the exact conflation the two-axis split was made to end. `NOT_APPLICABLE` names that state instead.

**A symbol stands in for the icon.** Page 14 asks each status to carry text, an icon and a reason. Text and reason are implemented; the icon is a character, because choosing an outline icon set is a decision the brandbook assigns to handoff and nobody has made it.

## Open, from the brandbook's own release list, p.24

- **Flat SVG logo master** — still not delivered. A flat *raster* master arrived on 2026-09-05 and is in use; the vector the brandbook specifies has not, so the mark cannot be scaled freely and there is no single-colour or 16 px variant to hand-check as page 4 requires.
- **An outline icon set** — not chosen.
- **Self-hosted WOFF2** — the stack names DejaVu first, per p.9, and falls back to system faces. No licence check has been run, so nothing is bundled.
- **A screen-reader pass with a real screen reader** — not run. What follows was checked programmatically, which is not the same thing.

## Page 23, run

Checked against the acceptance criteria, and five failed:

- **No skip link.** Added: a `.skip` anchor to `#content`, off-screen until focused.
- **No `aria-live`.** Added: the one-line run state is `aria-live="polite"`, and a failed write now goes to a `role="alert"` region that does not auto-dismiss, instead of a native `alert()`. p.23 asks for polite on a result and alert only for a blocker; an unsaved input is a blocker.
- **No `h1`.** The rail wordmark is now the `h1`. The artifact is a document inside a document, so its markdown headings are demoted one level — otherwise a run with a title produces a second `h1`.
- **A 28 px target.** The request disclosure was below the 44 px floor. Now `min-height: var(--control-height)`.
- **Reflow at 320 px was broken.** The page did not scroll sideways, which is what a naive check measures, but the 240 px rail left 120 px of main and the content overflowed inside it. There was no mobile layout at all. Below 768 px the rail is now a header: brand and run selector on one row, the section list as a scrolling row with its own area, options and key-value grids collapsed to one column, tables keeping their own scroll per p.19.

Verified after the fix at 320 × 800: no sideways page scroll, no inner overflow, every focusable at least 44 px tall, every control named, one `h1`, one `aria-live`, one `role="alert"`.

Still not done, and not claimable: keyboard-only operation by a person, an actual screen reader, and zoom to 200% on a real browser at a real size.

## The rule that does not move

**Nothing in the package depends on this running.** With the panel off you still have the run directory and the artifact, and that is the deliverable. No agent waits for it, polls it, or assumes anyone is watching.
