"use strict";

/* oratores run panel.
 *
 * Renders whatever is in run/<id>/ and writes back exactly two things: a
 * decided choice and a corrected assumption. Nothing here is required for the
 * skill to work.
 *
 * Follows Oratores_UI_Brandbook_v1: colour never carries meaning alone, so
 * every status renders its word; claim type is deliberately not a colour
 * dimension, because a type says nothing about whether anyone checked it.
 */

/* key, label, count, group. "you" needs a person; "work" is what the agents
   produced on the way, kept but not put in front of the decision. */
const SECTIONS = [
  ["choices",     "Decisions",   "you",  d => ((d.choices || {}).open || []).length],
  ["assumptions", "Assumptions", "you",  d => ((d.assumptions || {}).assumptions || []).filter(a => !a.corrected_to).length],
  ["findings",    "Problems",    "you",  d => ((d.findings || {}).findings || []).length],
  ["artifact",    "Draft",       "you",  d => (d.__artifact ? 1 : 0)],
  ["brief",       "Brief",       "work", d => (d.brief ? ((d.brief.segments || []).length || 1) : 0)],
  ["evidence",    "Evidence",    "work", d => ((d.evidence || {}).claims || []).length],
  ["objections",  "Objections",  "work", d => ((d.objections || {}).objections || []).length],
  ["candidates",  "Candidates",  "work", d => ((d.candidates || {}).sets || []).reduce((n, s) => n + (s.candidates || []).length, 0)],
];

const GROUP_LABEL = { you: "Needs you", work: "Working files" };

/* symbol, so the state never rides on hue alone */
const STATUS_SYMBOL = {
  CHECKED: "\u2713",
  CONFIRMED: "\u2713",
  UNVERIFIED: "?",
  CONTRADICTED: "\u2260",
  RECHECK: "\u21bb",
  NOT_APPLICABLE: "\u2014",
};

const AGENT_STATUS = {
  pending: "queued", running: "running", done: "done",
  failed: "failed", skipped: "skipped",
};

let runId = null;
let active = localStorage.getItem("oratores.section") || "choices";
let stream = null;
const navButtons = new Map();

const $ = sel => document.querySelector(sel);
const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text != null) n.textContent = text;
  return n;
};
const esc = s => String(s == null ? "" : s);
const isUnpriced = v => String(v || "").trim().toLowerCase() === "unpriced";

/* ----------------------------------------------------------------- theming */

function applyTheme(name) {
  document.documentElement.dataset.theme = name;
  localStorage.setItem("oratores.theme", name);
  $("#theme-toggle").textContent = name === "dark" ? "Light" : "Dark";
}

function initDetail() {
  const on = localStorage.getItem("oratores.detail") === "on";
  applyDetail(on);
  $("#detail-toggle").onclick = () =>
    applyDetail(document.body.dataset.detail !== "on");
}

function applyDetail(on) {
  document.body.dataset.detail = on ? "on" : "off";
  localStorage.setItem("oratores.detail", on ? "on" : "off");
  const b = $("#detail-toggle");
  b.textContent = on ? "Hide detail" : "Show detail";
  b.setAttribute("aria-pressed", String(on));
}

function initTheme() {
  const saved = localStorage.getItem("oratores.theme");
  const prefersLight = window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches;
  applyTheme(saved || (prefersLight ? "light" : "dark"));
  $("#theme-toggle").onclick = () =>
    applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
}

/* the run's state in one line, so the header does not read the task back at you */
function stateLine(d) {
  const open = ((d.choices || {}).open || []).length;
  const asm = ((d.assumptions || {}).assumptions || []).filter(a => !a.corrected_to).length;
  const gaps = ((d.assumptions || {}).blocking_gaps || []).length;
  const bad = ((d.findings || {}).findings || []).filter(f => f.direction === "severe").length;
  const agents = ((d.agents || {}).agents || []);
  const running = agents.filter(a => a.status === "running").map(a => a.name.replace(/^oratores-/, ""));
  const bits = [];
  if (open) bits.push(`${open} decision${open > 1 ? "s" : ""} open`);
  if (asm) bits.push(`${asm} assumption${asm > 1 ? "s" : ""} uncorrected`);
  if (gaps) bits.push(`${gaps} gap${gaps > 1 ? "s" : ""} left in the draft`);
  if (bad) bits.push(`${bad} problem${bad > 1 ? "s" : ""} that pass silently`);
  if (running.length) bits.push(`${running.join(", ")} still working`);
  return bits.length ? bits.join(" · ") : "Nothing waiting on you.";
}

/* -------------------------------------------------------------------- boot */

async function boot() {
  initTheme();
  initDetail();
  const res = await fetch("/api/runs").then(r => r.json());
  $("#schema-note").textContent = res.schema_checked ? "schema checking on" : "schema checking off";

  const sel = $("#run-select");
  sel.innerHTML = "";
  if (!res.runs.length) {
    sel.appendChild(el("option", null, "no runs yet"));
    return renderWelcome();
  }
  for (const r of res.runs) {
    const o = el("option", null, r.run_id);
    o.value = r.run_id;
    sel.appendChild(o);
  }
  sel.onchange = () => select(sel.value);

  const remembered = localStorage.getItem("oratores.run");
  select(res.runs.some(r => r.run_id === remembered) ? remembered : res.runs[0].run_id);
}

/* The brand layer is permitted here and only here — one motif, no editor. */
function renderWelcome() {
  $("#run-title").textContent = "No runs yet";
  $("#run-task").textContent = "";
  $("#nav").innerHTML = "";
  $("#s-choices").classList.add("on");
  const box = $("#choices-open");
  box.innerHTML = "";
  const w = el("div", "welcome");
  const img = el("img", "mark");
  img.src = "/mark.png";
  img.alt = "";
  img.width = 116;
  w.appendChild(img);
  w.appendChild(el("div", "word", "Oratores"));
  w.appendChild(el("h3", null, "Nothing to observe"));
  const p = el("p");
  p.innerHTML = "Start a run and it appears here within a second.";
  w.appendChild(p);
  w.appendChild(el("p", null, "The skill does not need this running. With the panel off you still have the run directory and the artifact, and that is the deliverable."));
  w.appendChild(el("div", "concept", "Flat raster master. The SVG master the brandbook asks for is still outstanding, so the mark is used at fixed sizes and never scaled up."));
  box.appendChild(w);
}

function select(id) {
  runId = id;
  localStorage.setItem("oratores.run", id);
  $("#run-select").value = id;
  if (stream) stream.close();
  stream = new EventSource(`/api/events?run=${encodeURIComponent(id)}`);
  stream.addEventListener("changed", load);
  stream.onopen = () => setLive(true);
  stream.onerror = () => setLive(false);
  load();
}

function setLive(on) {
  $("#live-dot").classList.toggle("live", on);
  $("#live-text").textContent = on ? "watching for changes" : "not connected";
}

/* -------------------------------------------------------------------- load */

async function load() {
  const p = await fetch(`/api/run/${encodeURIComponent(runId)}`).then(r => r.json());
  if (p.error) return;

  const d = {};
  for (const [name, val] of Object.entries(p.files || {})) d[name.replace(".json", "")] = val;
  d.__artifact = p.artifact;

  renderHead(d, p);
  renderNav(d);
  renderChoices(d.choices);
  renderAssumptions(d.assumptions);
  renderFindings(d.findings);
  renderBrief(d.brief);
  renderEvidence(d.evidence);
  renderObjections(d.objections);
  renderCandidates(d.candidates);
  renderArtifact(d.__artifact);
  show(active);
}

function renderHead(d, p) {
  const m = d.agents || {};
  $("#run-title").textContent = m.run_id || p.run_id;
  $("#run-state").textContent = stateLine(d);
  $("#run-task").textContent = [m.task, m.mode && `— ${m.mode}`, m.form && `· ${m.form}`]
    .filter(Boolean).join(" ");
  $("#task-fold").hidden = !m.task;

  /* agents are process, not decision: one line, and only in detail mode */
  const agents = m.agents || [];
  const doneCount = agents.filter(a => a.status === "done").length;
  const box = $("#agents");
  box.innerHTML = "";
  if (agents.length) {
    box.textContent = `${doneCount}/${agents.length} agents done`;
    box.title = agents
      .map(a => `${a.name} — ${AGENT_STATUS[a.status] || a.status}${a.note ? " (" + a.note + ")" : ""}`)
      .join("\n");
  }

  const probs = p.problems || [];
  $("#problems").hidden = probs.length === 0;
  const list = $("#problems-list");
  list.innerHTML = "";
  probs.forEach(x => list.appendChild(el("li", null, x)));
}

function renderNav(d) {
  const nav = $("#nav");
  nav.innerHTML = "";
  navButtons.clear();
  let group = null;
  for (const [key, label, g, count] of SECTIONS) {
    if (g !== group) {
      group = g;
      nav.appendChild(el("div", "nav-group", GROUP_LABEL[g]));
    }
    const n = count(d) || 0;
    const b = el("button", n ? "" : "empty");
    b.type = "button";
    b.appendChild(el("span", null, label));
    if (key !== "artifact") b.appendChild(el("span", "n", String(n)));
    b.onclick = () => {
      active = key;
      localStorage.setItem("oratores.section", key);
      show(key);
    };
    navButtons.set(key, b);
    nav.appendChild(b);
  }
}

function show(key) {
  if (!SECTIONS.some(s => s[0] === key)) key = SECTIONS[0][0];
  for (const [k] of SECTIONS) $(`#s-${k}`).classList.toggle("on", k === key);
  window.scrollTo(0, 0);
  for (const [k, b] of navButtons) b.setAttribute("aria-current", String(k === key));
}

/* p.23: aria-live polite for a result, role=alert for a blocker. A failed
   write is a blocker — your input was not saved — and it does not auto-dismiss. */
function blocker(msg) {
  const n = $("#alert");
  n.textContent = msg;
  n.hidden = false;
}

function clearBlocker() {
  $("#alert").hidden = true;
}

function emptyInto(node, msg) {
  node.innerHTML = "";
  const n = el("div", "empty-note");
  n.innerHTML = msg;
  node.appendChild(n);
}

/* ----------------------------------------------------------------- choices */

function renderChoices(c) {
  const openBox = $("#choices-open");
  openBox.innerHTML = "";
  const open = (c && c.open) || [];
  if (!open.length) emptyInto(openBox, "Nothing to decide. Every choice so far was either made or defaulted \u2014 the defaults are under Assumptions.");

  for (const ch of open) {
    const card = el("div", "choice");
    const head = el("header");
    head.appendChild(el("div", "q", ch.question));
    const meta = el("div", "meta");
    if (ch.procedure) meta.appendChild(el("span", "tag pid tech", ch.procedure));
    if (ch.raised_by) meta.appendChild(el("span", "tag tech", ch.raised_by));
    if (ch.conflict) {
      const who = (ch.conflict.between || []).map(x => x.replace(/^oratores-/, ""));
      const t = el("span", "tag conflict", `${who.join(" and ")} disagree`);
      t.title = ch.conflict.about || "";
      meta.appendChild(t);
    }
    head.appendChild(meta);
    if (ch.conflict && ch.conflict.about) {
      const det = el("details");
      det.appendChild(el("summary", null, "Why you are being asked instead of told"));
      det.appendChild(el("p", "why", ch.conflict.about));
      head.appendChild(det);
    }
    card.appendChild(head);

    const opts = el("div", "opts");
    for (const o of ch.options || []) {
      const box = el("div", "opt" + (ch.recommended === o.label ? " rec" : ""));
      const lbl = el("div", "lbl");
      lbl.appendChild(el("span", null, o.label));
      if (ch.recommended === o.label) lbl.appendChild(el("span", "tag", "recommended"));
      if (o.sourced === false) lbl.appendChild(el("span", "tag unsourced", "judgement"));
      box.appendChild(lbl);

      const dl = el("dl");
      const row = (k, v, cls) => {
        if (!v) return;
        dl.appendChild(el("dt", null, k));
        dl.appendChild(el("dd", cls, v));
      };
      row("effect", o.effect);
      if (isUnpriced(o.cost)) {
        dl.appendChild(el("dt", null, "cost"));
        const dd = el("dd", "secondary");
        dd.appendChild(el("span", "tag unpriced", "unpriced"));
        dd.appendChild(el("span", null, " — no source states one. Unknown, not free."));
        dl.appendChild(dd);
      } else {
        row("cost", o.cost);
      }
      row("use when", o.condition, "secondary");
      box.appendChild(dl);
      box.appendChild(el("div", "spacer"));

      const btn = el("button", "pick", "Choose");
      btn.type = "button";
      btn.onclick = async () => {
        btn.disabled = true;
        btn.textContent = "Writing…";
        const r = await fetch(`/api/run/${encodeURIComponent(runId)}/decide`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id: ch.id, chose: o.label }),
        }).then(x => x.json()).catch(e => ({ ok: false, error: String(e) }));
        if (!r.ok) {
          btn.disabled = false;
          btn.textContent = "Choose";
          blocker(r.error || "Could not save that choice. Nothing was written; the decision is still open.");
        } else {
          clearBlocker();
        }
      };
      box.appendChild(btn);
      opts.appendChild(box);
    }
    card.appendChild(opts);
    openBox.appendChild(card);
  }

  const dec = (c && c.decided) || [];
  $("#choices-decided-card").hidden = dec.length === 0;
  const db = $("#choices-decided");
  db.innerHTML = "";
  for (const x of dec) {
    const row = el("div", "decided");
    row.appendChild(el("span", "chose", x.chose));
    if ((x.rejected || []).length) row.appendChild(el("span", "rej", (x.rejected || []).join(", ")));
    row.appendChild(el("span", null, x.question || ""));
    row.appendChild(el("span", "who", `${x.by || "?"}${x.at ? " · " + x.at.slice(0, 16).replace("T", " ") : ""}`));
    db.appendChild(row);
  }
}

/* ------------------------------------------------------------- assumptions */

function renderAssumptions(a) {
  const box = $("#assumptions");
  box.innerHTML = "";
  const items = (a && a.assumptions) || [];
  if (!items.length) emptyInto(box, "Nothing was assumed. Every input needed was supplied.");

  for (const x of items) {
    const n = el("div", "asm");
    n.dataset.c = x.confidence || "safe";
    const head = el("div", "input");
    head.appendChild(el("span", null, x.input));
    /* confidence as a word, so the coloured edge is reinforcement only */
    if (x.confidence) head.appendChild(el("span", "tag", x.confidence));
    n.appendChild(head);
    n.appendChild(el("div", "assumed", `assumed: ${x.assumed}`));
    const why = [x.because, x.changes_what && `moves: ${x.changes_what}`].filter(Boolean).join(" · ");
    if (why) n.appendChild(el("div", "why", why));
    if (x.corrected_to) {
      const at = x.corrected_at ? ` · ${x.corrected_at.slice(0, 16).replace("T", " ")}` : "";
      n.appendChild(el("div", "corrected", `corrected to: ${x.corrected_to}${at}`));
    }

    const fix = el("div", "fix");
    const inp = el("input");
    inp.type = "text";
    inp.setAttribute("aria-label", `Correct: ${x.input}`);
    inp.placeholder = x.corrected_to ? "change the correction…" : "the real value…";
    const btn = el("button", "pick ghost", "Correct");
    btn.type = "button";
    btn.onclick = async () => {
      const r = await fetch(`/api/run/${encodeURIComponent(runId)}/assumption`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: x.id, corrected_to: inp.value.trim() }),
      }).then(v => v.json()).catch(e => ({ ok: false, error: String(e) }));
      if (!r.ok) blocker(r.error || "Could not save that correction. Nothing was written; the assumption still reads as it did.");
      else clearBlocker();
    };
    inp.onkeydown = e => { if (e.key === "Enter") btn.click(); };
    fix.appendChild(inp);
    fix.appendChild(btn);
    n.appendChild(fix);
    box.appendChild(n);
  }

  const gaps = (a && a.blocking_gaps) || [];
  $("#gaps-card").hidden = gaps.length === 0;
  const gb = $("#gaps");
  gb.innerHTML = "";
  for (const g of gaps) {
    const n = el("div", "asm");
    n.dataset.c = "blocking";
    n.appendChild(el("div", "input", g.input));
    n.appendChild(el("div", "assumed", `left as: ${g.specified_as}`));
    if (g.cannot_be_defaulted_because) n.appendChild(el("div", "why", g.cannot_be_defaulted_because));
    gb.appendChild(n);
  }
}

/* ---------------------------------------------------------------- findings */

function renderFindings(f) {
  const box = $("#findings");
  box.innerHTML = "";
  /* severity is a rank: 1 is the worst finding in the run */
  const items = ((f && f.findings) || []).slice().sort((a, b) => (a.severity || 99) - (b.severity || 99));
  if (!items.length) emptyInto(box, "No problems found \u2014 either nothing has been reviewed yet, or nothing survived checking.");

  for (const x of items) {
    const n = el("div", "finding");
    const top = el("div", "top");
    if (x.severity != null) top.appendChild(el("span", "tag rank", `#${x.severity}`));
    top.appendChild(el("span", `tag ${x.verdict}`, x.verdict));
    if (x.direction) top.appendChild(el("span", "tag", x.direction));
    top.appendChild(el("span", "claim", x.claim));
    n.appendChild(top);
    if (x.failure) n.appendChild(el("div", "fail", x.failure));
    if (x.anchor) {
      const a = x.anchor;
      const where = [a.file, a.line != null && `:${a.line}`, a.slide != null && ` slide ${a.slide}`]
        .filter(Boolean).join("");
      n.appendChild(el("div", "anchor", where + (a.quote ? `  “${a.quote}”` : "")));
    }
    if (x.smallest_fix) {
      const fx = el("div", "fix");
      fx.appendChild(el("b", null, "Smallest fix: "));
      fx.appendChild(el("span", null, x.smallest_fix));
      n.appendChild(fx);
    }
    box.appendChild(n);
  }

  const nr = (f && f.not_reviewed) || [];
  const cov = (f && f.coverage) || [];
  $("#notreviewed-card").hidden = nr.length === 0 && cov.length === 0;
  const cb = $("#coverage");
  cb.innerHTML = "";
  if (cov.length) {
    cb.appendChild(el("h4", null, "Reviewed"));
    cov.forEach(x => cb.appendChild(el("div", "decided", x)));
  }
  const nb = $("#notreviewed");
  nb.innerHTML = "";
  if (nr.length) {
    nb.appendChild(el("h4", null, "Not reviewed"));
    nr.forEach(x => nb.appendChild(el("div", "decided", x)));
  }
}

/* ------------------------------------------------------------------- brief */

function renderBrief(b) {
  const box = $("#brief");
  box.innerHTML = "";
  if (!b) return emptyInto(box, "No brief yet.");

  const kv = (title, pairs) => {
    if (!pairs.some(([, v]) => v != null && v !== "")) return;
    const c = el("div", "card");
    c.appendChild(el("h4", null, title));
    const dl = el("dl", "kv");
    for (const [k, v] of pairs) {
      if (v == null || v === "") continue;
      dl.appendChild(el("dt", null, k));
      dl.appendChild(el("dd", null, Array.isArray(v) ? v.join(" · ") : String(v)));
    }
    c.appendChild(dl);
    box.appendChild(c);
  };

  const o = b.objective || {};
  kv("Objective", [
    ["audience", o.audience],
    ["change", o.change],
    ["behaviour", o.specific_behaviour],
    ["success metric", o.success_metric == null ? "not stated — absent, not invented" : o.success_metric],
    ["heard before", b.heard_before],
  ]);

  if (b.contested) kv("What is contested", [
    ["lens", b.contested.lens],
    ["finding", b.contested.finding],
    ["sentence to decide", b.contested.question_to_decide],
  ]);

  if ((b.segments || []).length) {
    const c = el("div", "card");
    c.appendChild(el("h4", null, `Segments — writing to “${b.primary_segment || "not chosen"}”`));
    const t = el("table");
    t.innerHTML = "<thead><tr><th>segment</th><th>believes</th><th>fears</th><th>realistic action</th><th>intensity</th></tr></thead>";
    const tb = el("tbody");
    for (const s of b.segments) {
      const tr = el("tr", s.name === b.primary_segment ? "primary" : null);
      const name = el("td");
      name.appendChild(el("strong", null, s.name));
      if (s.size) name.appendChild(el("div", "d", s.size));
      tr.appendChild(name);
      [s.believes, s.fears, s.realistic_action].forEach(v => tr.appendChild(el("td", null, esc(v))));
      const it = el("td");
      if (s.intensity) it.appendChild(el("span", "chip", s.intensity));
      tr.appendChild(it);
      tb.appendChild(tr);
    }
    t.appendChild(tb);
    c.appendChild(t);
    box.appendChild(c);
  }

  const r = b.resistance || {};
  kv("Resistance", [["kind", r.kind], ["dominant", r.dominant], ["anchor to", r.anchor], ["sacrifice named", r.sacrifice_named]]);

  const a = b.ask || {};
  kv("The ask", [["one step", a.one_step], ["owner", a.owner], ["boundary", a.boundary],
                 ["how we know", a.how_we_know], ["whole product", a.whole_product]]);

  const u = b.urgency || {};
  kv("Urgency", [["state", u.state], ["complacency", u.complacency_sources], ["levers", u.levers]]);
}

/* ---------------------------------------------------------------- evidence */

function renderEvidence(e) {
  const box = $("#evidence");
  box.innerHTML = "";
  if (!e) return emptyInto(box, "No evidence gathered yet.");

  const claims = e.claims || [];
  const c = el("div", "card");
  if (!claims.length) {
    c.appendChild(el("h4", null, "No checkable claim"));
    c.appendChild(el("div", "why", "The piece rests on no claim anyone could check. That is a state, not an empty field."));
  } else {
    const t = el("table");
    t.innerHTML = "<thead><tr><th>id</th><th>claim</th><th>type</th><th>source status</th><th>source</th><th>checked first</th></tr></thead>";
    const tb = el("tbody");
    for (const x of claims) {
      const tr = el("tr");
      tr.appendChild(el("td", "id", x.id));
      tr.appendChild(el("td", null, x.text));

      /* axis 1 — what kind of claim. Neutral: hue here would encode the wrong thing. */
      const ty = el("td");
      ty.appendChild(el("span", "chip type", x.label));
      tr.appendChild(ty);

      /* axis 2 — whether anyone checked it. Coloured, and always worded. */
      const st = el("td");
      const status = x.source_status;
      if (status) {
        const chip = el("span", `chip status-${status}`);
        chip.appendChild(el("span", "sym", STATUS_SYMBOL[status] || "\u00b7"));
        chip.appendChild(el("span", null, status.replace(/_/g, " ").toLowerCase()));
        st.appendChild(chip);
        if (x.source_status_reason) st.appendChild(el("div", "d", x.source_status_reason));
      } else {
        st.appendChild(el("span", "chip", "not stated"));
      }
      tr.appendChild(st);

      const s = el("td", null, [x.source, x.population, x.date].filter(Boolean).join(" · ") || "—");
      if (x.locator) s.appendChild(el("div", "d", x.locator));
      if (x.comparator_chosen_before_direction === null && x.comparator) {
        s.appendChild(el("div", "d", "comparator timing not recorded"));
      }
      tr.appendChild(s);

      const rk = el("td");
      if (x.checked_first_risk) rk.appendChild(el("span", `chip ${x.checked_first_risk}`, x.checked_first_risk));
      tr.appendChild(rk);
      tb.appendChild(tr);
    }
    t.appendChild(tb);
    c.appendChild(t);
  }
  box.appendChild(c);

  if ((e.gaps || []).length) {
    const g = el("div", "card");
    g.appendChild(el("h4", null, "Gaps — named, not filled"));
    for (const x of e.gaps) {
      const n = el("div", "decided");
      n.appendChild(el("span", "chose", x.id || ""));
      n.appendChild(el("span", null, x.needed));
      n.appendChild(el("span", "who", x.who_could_supply || ""));
      g.appendChild(n);
      if (x.why_it_matters) g.appendChild(el("div", "why", x.why_it_matters));
    }
    box.appendChild(g);
  }

  if ((e.unusable || []).length) {
    const u = el("div", "card");
    u.appendChild(el("h4", null, "Rejected — recorded so nobody rediscovers it"));
    for (const x of e.unusable) {
      const n = el("div", "decided");
      n.appendChild(el("span", "rej", x.text));
      n.appendChild(el("span", "who", x.reason || ""));
      u.appendChild(n);
    }
    box.appendChild(u);
  }
}

/* -------------------------------------------------------------- objections */

function renderObjections(o) {
  const box = $("#objections");
  box.innerHTML = "";
  if (!o) return emptyInto(box, "No objections mapped yet.");

  const c = el("div", "card");
  const t = el("table");
  t.innerHTML = "<thead><tr><th>objection</th><th>charitable reading</th><th>correct?</th><th>response</th><th>limitation</th><th>where</th></tr></thead>";
  const tb = el("tbody");
  for (const x of o.objections || []) {
    const tr = el("tr");
    const first = el("td");
    first.appendChild(el("strong", null, x.objection));
    if (x.who_holds_it) first.appendChild(el("div", "d", x.who_holds_it));
    if (x.underlying_fear) first.appendChild(el("div", "d", `fear: ${x.underlying_fear}`));
    tr.appendChild(first);
    tr.appendChild(el("td", null, esc(x.charitable_reading)));
    const ok = el("td");
    if (x.is_it_correct) ok.appendChild(el("span", `chip ${x.is_it_correct}`, x.is_it_correct));
    tr.appendChild(ok);
    const rsp = el("td", null, esc(x.response));
    if (x.next_action) rsp.appendChild(el("div", "d", `then: ${x.next_action}`));
    tr.appendChild(rsp);
    const lim = el("td");
    if (x.limitation) lim.textContent = x.limitation;
    else lim.appendChild(el("span", "chip status-UNVERIFIED", "? none stated"));
    tr.appendChild(lim);
    tr.appendChild(el("td", null, esc(x.where)));
    tb.appendChild(tr);
  }
  t.appendChild(tb);
  c.appendChild(t);
  box.appendChild(c);

  if ((o.mechanism_carrying || []).length) {
    const m = el("div", "card");
    m.appendChild(el("h4", null, "What is carrying each passage"));
    const t2 = el("table");
    t2.innerHTML = "<thead><tr><th>passage</th><th>mechanism</th><th>its cost</th><th>alternative</th></tr></thead>";
    const tb2 = el("tbody");
    for (const x of o.mechanism_carrying) {
      const tr = el("tr");
      tr.appendChild(el("td", null, x.passage));
      tr.appendChild(el("td", null, x.mechanism));
      const ct = el("td");
      if (isUnpriced(x.stated_cost)) ct.appendChild(el("span", "tag unpriced", "unpriced"));
      else ct.textContent = esc(x.stated_cost);
      tr.appendChild(ct);
      tr.appendChild(el("td", null, [x.alternative, x.alternative_cost].filter(Boolean).join(" — ")));
      tb2.appendChild(tr);
    }
    t2.appendChild(tb2);
    m.appendChild(t2);
    box.appendChild(m);
  }

  if (o.dissent_position) {
    const d = o.dissent_position;
    const n = el("div", "card");
    n.appendChild(el("h4", null, "Dissent scale"));
    n.appendChild(el("div", null, `position ${d.position}, rejecting ${d.rejected}${d.why ? " — " + d.why : ""}`));
    box.appendChild(n);
  }
}

/* -------------------------------------------------------------- candidates */

function renderCandidates(c) {
  const box = $("#candidates");
  box.innerHTML = "";
  if (!c) return emptyInto(box, "Nothing generated yet.");

  for (const s of c.sets || []) {
    const card = el("div", "card cand-set");
    card.appendChild(el("h4", null, `For: ${s.for}`));
    const list = s.candidates || [];
    const kept = new Set(s.kept || []);
    card.appendChild(el("div", "gen",
      `generator: ${s.generator} · ${list.length} generated, ${kept.size} kept` +
      (s.first_refused ? " · first refused" : "")));
    for (const x of list) {
      /* kept is a list of ids, never of candidate text */
      const status = x.status || (kept.has(x.id) ? "kept" : "open");
      const n = el("div", `cand ${status}`);
      n.appendChild(el("div", "t", x.text));
      const meta = [
        x.id,
        status !== "open" ? status : null,
        x.device,
        x.survives_paraphrase === false ? "wording-bound" : null,
        x.note,
      ].filter(Boolean).join(" · ");
      if (meta) n.appendChild(el("div", "d", meta));
      card.appendChild(n);
    }
    box.appendChild(card);
  }
}

/* ---------------------------------------------------------------- artifact */

function renderArtifact(md) {
  const box = $("#artifact");
  if (!md) { box.innerHTML = '<div class="empty-note">No draft yet.</div>'; return; }
  box.innerHTML = mdToHtml(md);
}

function mdToHtml(src) {
  const escape = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const inline = s => escape(s)
    .replace(/\[gap:([^\]]*)\]/g, '<span class="gap">gap:$1</span>')
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[^*])\*([^*]+)\*/g, "$1<em>$2</em>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");

  const out = [];
  let list = null, quote = null;
  const flush = () => {
    if (list) { out.push(`<ul>${list.join("")}</ul>`); list = null; }
    if (quote) { out.push(`<blockquote>${quote.join("")}</blockquote>`); quote = null; }
  };
  for (const raw of src.split(/\r?\n/)) {
    const line = raw.trimEnd();
    const h = /^(#{1,3})\s+(.*)$/.exec(line);
    const li = /^\s*[-*]\s+(.*)$/.exec(line);
    const bq = /^>\s?(.*)$/.exec(line);
    if (li) { if (quote) flush(); list = list || []; list.push(`<li>${inline(li[1])}</li>`); continue; }
    if (bq) { if (list) flush(); quote = quote || []; quote.push(`<p>${inline(bq[1])}</p>`); continue; }
    flush();
    if (/^(-{3,}|\*{3,}|_{3,})$/.test(line)) { out.push("<hr>"); continue; }
    /* the artifact is a document inside a document: demote its headings one
       level so the page keeps a single h1 */
    if (h) { const lvl = Math.min(h[1].length + 1, 6); out.push(`<h${lvl}>${inline(h[2])}</h${lvl}>`); continue; }
    if (!line) continue;
    out.push(`<p>${inline(line)}</p>`);
  }
  flush();
  return out.join("\n");
}

boot();
