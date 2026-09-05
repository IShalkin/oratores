# Data Storytelling — DAT

Turning a dataset into a communication. The distinction that organizes everything here: **exploratory** analysis is opening a hundred oysters to find two pearls; **explanatory** communication is presenting the two pearls. Showing raw exploratory output makes the audience reopen all hundred oysters, which is the most common failure in data-heavy presentation and is almost always mistaken for thoroughness.

---

## DAT-01 — Context before pixels

**Trigger.** Before opening any charting tool.

**Procedure.** In this strict order:

1. **Who.** One specific audience, ideally the person who decides. Not "internal and external stakeholders". Then assess your own standing with them, because it changes how directly you can state a conclusion.
2. **What.** The action you need them to know or do. If you cannot articulate it, question whether to communicate at all. Take a position — you are the person who looked at the data, and an audience handed a blank slate resents it. Where an explicit recommendation is not yours to make, propose next steps so they have something to react to.
3. **How.** Only now: what data supports the point. Data is supporting evidence, not the story.
4. Identify the **mechanism**, because it changes the artifact:
   - **Live presentation** — you control the pace, so slides can be sparse and detail can live in your mouth. No tables.
   - **Circulated document** — they control consumption, so every so-what must be explicit on the page and each visual must be annotated.
   - Both from one artifact — layer states on one slide with simple appear/disappear, and put the fully annotated version on top so the export stands alone.
5. Compress the message: a three-minute version, then one sentence containing your point of view and what is at stake. Then storyboard on paper or sticky notes. **Never start in the presentation tool** — a digital draft creates an attachment that resists the cuts you will need.

**Gates.**
- Who / what / how done in that order.
- A stated action, or an explicit statement that none is being asked.
- Mechanism identified before design.
- Storyboard exists on paper.

**Failure signals.**
- Charts built before the message is written.
- "Here's what the data shows" as the entire framing.
- The audience's reaction is "interesting" — you never asked for anything.
- Exploratory output shown as a finding.

---

## DAT-02 — Choose the display

**Trigger.** Once the message is articulated.

**Procedure.** A small set of forms covers almost everything. Choose by what the message is:

- **One or two numbers** → simple text. The number large, a few words around it. Having numbers is not a reason to make a graph.
- **Each audience member wants to find their own row, or units differ** → a table, with minimal borders or none.
- **Table detail plus magnitude at a glance** → a heatmap, single-hue saturation, with a legend.
- **Relationship between two variables** → scatterplot.
- **Continuous, over time** → line graph. Two time points across many categories → a slopegraph. Forecast included → solid line for actual, thin dotted for forecast, and label both.
- **Categorical** → **horizontal bar** is the default: it handles long labels and the reading path hits the name before the data. Totals plus components → stacked bar. A negative-to-positive scale → 100% stacked horizontal bar. Start value, changes, end value → waterfall.
- **Vastly different magnitudes** → square area.

Hard rules:

1. **Bar charts start at zero, always.** Eyes compare endpoints; truncating a bar axis is not emphasis, it is a false statement.
2. Line graphs may use a non-zero baseline, with care, because position rather than length carries the meaning — but flag it and do not over-zoom.
3. **No pies, no donuts, no 3D, no secondary axes.** Replace a pie with a sorted horizontal bar plus a "total 100%" note. Replace a secondary axis by labelling those points directly, or by splitting into two panels sharing one x-axis.
4. Never remove 3D "for looks" — remove it because depth distorts the values.
5. Where categories have a natural order (ages, time, an ordinal scale), keep it. Where they do not, sort by value. Once an audience has learned a chart, shift emphasis but **never re-sort** — re-sorting makes them relearn it.
6. The right chart is whatever is easiest for **this** audience to read. Test it: show a colleague and have them narrate where their eyes go, what they see, and what they would ask.

**Gates.**
- Zero baseline on every bar chart.
- No pie, donut, 3D, or secondary axis.
- The chart type is named with the message it carries, and with the type rejected.
- Tested on one person who was not involved.

**Failure signals.**
- Multiple similar pies — switch to a matrix or bars.
- A rainbow scale encoding rank.
- Trailing zeros, diagonal labels, a bordered legend at the bottom with the data at the top.
- Default output from the tool: border, gridlines, markers, multi-colour. The tool decided, not you.

---

## DAT-03 — Declutter, then focus

**Trigger.** Every chart built from tool defaults.

**Procedure.**

1. **Declutter.** Every element consumes attention; what decides your fate is how hard the visual *looks*. Remove the chart border → remove or thin and grey the gridlines → remove default markers → clean axis labels (strip trailing zeros, abbreviate to avoid rotated text) → label series directly and delete the legend → colour each label to match its series.
   Keep currency symbols, percent signs and commas. That redundancy reduces load rather than adding it.
2. Ask of each remaining element: *would removing this change anything?* If no, remove it. Grouping is often supplied free by spacing, by shared colour, or by a light shaded region — so the border, the background fill and the axis line are usually unnecessary.
3. **Then focus.** Push everything to the background first — grey the whole visual — and explicitly earn each element back into the foreground with colour, weight, size, a marker or a label.
4. Use the attributes that actually pre-attentively encode quantity: **length and spatial position**. Hue does not encode quantity — "which is greater, red or blue" is not a question. Saturation of a single hue does.
5. Default palette: shades of grey plus one bold accent. Grey rather than black as the base, so the accent contrasts more. Keep the accent consistent across the whole deck.
6. Position: the audience starts top-left and scans in a Z. Put the most important thing there.
7. **Add the text layer.** Every chart needs a title; every axis needs a title; the conclusion goes in words on the slide; annotate the specific point with the cause, the nuance, or the external factor. Omitting an axis title is a rare and deliberate move.
8. Validate: look away, look back, and check where your eyes land first. Then have someone with no context narrate it.

**Gates.**
- Decluttering pass run.
- Everything greyed, then earned forward.
- Conclusion stated in words on the visual.
- Eye-draw test passed.

**Failure signals.**
- You are tracing the chart with your finger — spacing or proximity is wrong.
- Your eyes dart with nowhere to land — the contrast is non-strategic.
- The title describes instead of asserting.
- Space remained, so more data was added.

---

## DAT-04 — Narrative over a dataset

**Trigger.** The data must persuade, not merely inform.

**Procedure.**

1. Build the three acts:
   - **Beginning** — the setting, the main character (which is the audience), the imbalance, the balance they want, and why they should pay attention now.
   - **Middle** — background, external comparison, examples, the data, the cost of doing nothing, the options, the benefits, and why this audience is uniquely positioned.
   - **End** — the explicit call to action, tied back to the tension you opened with.
2. The tension is the conflict between what is and what could be. If you think you have no problem, you have no tension and no story — go back and reconsider, because there almost always is one.
3. Announce the narrative order and stick to it: chronological (problem → data → analysis → finding → recommendation) when you need to build credibility or the audience cares about the method; conclusion-first when trust exists and they want the answer. Say which you are doing.
4. Repeat deliberately: state what you will show, show it, then summarize what it means. This feels redundant to you and reassuring to an audience that is not close to the content.
5. Run the two logic checks:
   - **Horizontal logic** — read only the slide titles in order. Do they tell the story on their own?
   - **Vertical logic** — is each slide internally self-reinforcing, with nothing extraneous?
6. **Reverse-storyboard** the finished artifact: flip through and write down each page's main point. The list should match your intended outline. Where it does not, the artifact is not what you think it is.
7. Where one dataset carries several stories, build one base visual, walk the audience through it unhighlighted, then highlight each story in turn — and never re-sort between them.

**Gates.**
- Three acts present, with the audience as protagonist.
- Real tension named.
- Horizontal and vertical logic both pass.
- Reverse storyboard matches the intended outline.

**Failure signals.**
- Data presented in the order it was analyzed.
- A finding with no call to action.
- Slide titles that, read together, are a table of contents.
- An iteration that disproves your headline — rewrite the headline, not the data.

---

## Defaults and thresholds

| Decision | Default |
|---|---|
| Audience | one, named, ideally the decider |
| Chart for 1–2 numbers | none; state the number |
| Bar chart baseline | zero, always |
| Palette | greys + 1 accent |
| Highlighted share | ≤ ~10% |
| Chunks an audience holds | ~4; beyond that, label directly |
| Window before they decide whether to keep looking | 3–8 seconds |
| Rotated text | never; 45° reads about half as fast |
| Colour vision deficiency | ~8% of men; check greyscale and red/green |
| Storyboard medium | paper or sticky notes, never the tool |

---

## Related

`LOG-02` handles the spoken form of a number and the comparator problem. `VIS-02` and `VIS-03` handle the slide the chart sits on. `MSG-01` supplies the one-sentence message this module presupposes. `LOG-04` labels the claim the chart makes. `REV-02` runs the same logic checks across the whole artifact.
