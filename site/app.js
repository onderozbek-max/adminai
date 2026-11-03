(() => {
  "use strict";
  const DATA = window.SURVEYCOACH_DEMO;
  const READINESS = { ready: "Ready to launch", almost_ready: "Almost ready", needs_work: "Needs work" };
  const SEVERITY = { must_fix: "Must fix", worth_improving: "Worth improving" };
  const state = { survey: 0, filter: "all", selected: null, page: 0 };
  const $ = (id) => document.getElementById(id);

  // Build DOM with textContent only: sample data can never inject markup.
  function h(tag, attrs, ...kids) {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === false || v == null) continue;
      if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? "" : v);
    }
    for (const kid of kids.flat(Infinity)) if (kid != null && kid !== false) el.append(kid.nodeType ? kid : document.createTextNode(kid));
    return el;
  }
  const current = () => DATA.surveys[state.survey];
  // replaceChildren() would print "false" for `cond && element`, so every render goes through here.
  const mount = (el, ...kids) => el.replaceChildren(...kids.flat(Infinity).filter(Boolean));
  const say = (text) => { $("status").textContent = text; };
  const crit = (id) => DATA.criteria[id] || { title: id };

  function pageIndexOf(finding, snapshot) {
    if (finding.page_id) return snapshot.pages.findIndex((p) => p.id === finding.page_id);
    if (finding.question_id) return snapshot.pages.findIndex((p) => (p.questions || []).some((q) => q.id === finding.question_id));
    return -1;
  }
  const whereLabel = (f, snapshot) => {
    const i = pageIndexOf(f, snapshot);
    return i < 0 ? "Whole survey" : `Screen ${i + 1}`;
  };

  /* ---------- summary ---------- */
  function renderSummary() {
    const { review } = current(), card = review.scorecard;
    const dims = Object.values(card.by_dimension).map((d) =>
      h("li", null, h("span", null, d.name),
        h("meter", { min: 0, max: d.possible, value: d.earned, "aria-label": `${d.name}: ${d.earned.toFixed(1)} of ${d.possible} points` }),
        h("span", { class: "num" }, `${d.earned.toFixed(1)} / ${d.possible}`)));
    const promise = review.promised_minutes ? ` (the intro promises ${review.promised_minutes})` : "";
    mount($("summary"), 
      h("h2", { id: "summary-h" }, "Review summary"),
      h("span", { class: `badge ${card.readiness}` }, READINESS[card.readiness]),
      h("p", { class: "score" }, card.score.toFixed(1), h("small", null, ` out of 100${card.provisional ? " (provisional)" : ""}`)),
      card.provisional && h("p", { class: "note" }, `${card.unchecked_points} of the 100 points are judged by the AI step, which has not run on this sample, so they count as full credit for now.`),
      card.open_blockers.length > 0 && h("p", { class: "note" }, h("strong", null, "Must fix before launch: "), card.open_blockers.map((b) => `${b} ${crit(b).title}`).join("; ")),
      card.pending_blockers.length > 0 && h("p", { class: "note" }, `Blockers ${card.pending_blockers.join(", ")} need the AI step, so this cannot be called Ready to launch yet.`),
      h("p", { class: "note" }, `Members will need about ${review.est_minutes} minutes${promise}. This is an estimate.`),
      h("h3", null, "Score by area"), h("ul", { class: "dims" }, dims));
  }

  /* ---------- findings ---------- */
  const visibleFindings = () => current().review.findings
    .map((f, index) => ({ f, index })).filter(({ f }) => state.filter === "all" || f.severity === state.filter);

  function renderFindings() {
    const { review, snapshot } = current(), all = review.findings;
    const count = (sev) => all.filter((f) => f.severity === sev).length;
    const filters = [["all", `All (${all.length})`], ["must_fix", `Must fix (${count("must_fix")})`], ["worth_improving", `Worth improving (${count("worth_improving")})`]]
      .map(([key, label]) => h("button", { type: "button", "aria-pressed": String(state.filter === key), onclick: () => setFilter(key) }, label));
    const items = visibleFindings().flatMap(({ f, index }) => {
      const open = state.selected === index;
      const row = h("li", { class: f.severity },
        h("button", { type: "button", class: "row", "data-idx": index, "aria-expanded": String(open), "aria-controls": open ? "finding-detail" : false, onclick: () => selectFinding(index) },
          h("span", { class: "tag" }, SEVERITY[f.severity]), " ", h("strong", null, crit(f.criterion_id).title),
          h("div", { class: "crit" }, `Rubric ${f.criterion_id} \u2022 ${whereLabel(f, snapshot)}`),
          h("div", null, f.evidence)));
      return open ? [row, h("li", { class: "detail-item" }, renderDetail())] : [row];
    });
    mount($("findings"), 
      h("h2", { id: "findings-h" }, `Findings (${all.length})`),
      h("div", { class: "filters", role: "group", "aria-label": "Filter findings" }, filters),
      state.selected == null && h("p", { class: "note" }, "Select a finding to see the fix and jump to that screen on the phone."),
      items.length ? h("ul", { class: "finding-list" }, items) : h("p", { class: "note" }, "Nothing here. This sample has no findings in this group."),
      h("div", { class: "lists" },
        h("h3", null, "What is working"), h("ul", null, (review.scorecard.strengths.length ? review.scorecard.strengths : ["Nothing stands out yet."]).map((s) => h("li", null, s))),
        h("h3", null, "Waiting on the AI step"), h("ul", null, review.unchecked.map((s) => h("li", null, s)))));
  }

  function renderDetail() {
    const { review, snapshot } = current(), f = review.findings[state.selected], msg = h("p", { class: "note", role: "status" });
    return h("div", { class: "detail", id: "finding-detail" },
      h("h3", null, crit(f.criterion_id).title),
      h("dl", null,
        h("dt", null, "Where"), h("dd", null, whereLabel(f, snapshot)),
        h("dt", null, "What we found"), h("dd", null, f.evidence),
        h("dt", null, "How to fix it"), h("dd", null, f.explanation),
        h("dt", null, "Why it matters to members"), h("dd", null, f.member_impact)),
      h("div", { class: "actions" },
        h("button", { type: "button", class: "copy", onclick: () => copyFix(f.explanation, msg) }, "Copy suggestion"),
        h("button", { type: "button", onclick: showOnPhone }, "Show on phone")),
      msg);
  }

  function showOnPhone() {
    const heading = $("phone-h");
    heading.setAttribute("tabindex", "-1");
    heading.scrollIntoView({ block: "start" });
    heading.focus();
  }

  function backToFinding() {
    const button = document.querySelector(`[data-idx="${state.selected}"]`);
    if (button) { button.scrollIntoView({ block: "center" }); button.focus(); }
  }

  async function copyFix(text, msg) {
    try {
      await navigator.clipboard.writeText(text);
      msg.textContent = "Copied. Paste it into RedJade yourself: SurveyCoach does not change your survey.";
    } catch (_) {
      msg.textContent = "Copy is not available in this browser. Select the suggestion text above and copy it.";
    }
  }

  function setFilter(key) {
    state.filter = key;
    renderFindings();
    document.querySelector('.filters [aria-pressed="true"]').focus();
  }

  function selectFinding(index) {
    state.selected = index;
    const target = pageIndexOf(current().review.findings[index], current().snapshot);
    if (target >= 0) state.page = target;
    renderFindings(); renderPhone();
    document.querySelector(`[data-idx="${index}"]`).focus();
    const flagged = document.querySelector(".q.selected");
    if (flagged) flagged.scrollIntoView({ block: "nearest" });
  }

  /* ---------- phone ---------- */
  const points = (scale) => Array.from({ length: scale.points }, (_, i) => (scale.points === 11 ? i : i + 1));
  const ratio = (m) => (m.natural_w && m.natural_h ? `${m.natural_w} / ${m.natural_h}` : "1 / 1");

  function mediaBox(m) {
    if (m.loaded === false) return h("div", { class: "media broken", role: "img", "aria-label": "Image failed to load" }, "Image failed to load");
    return h("div", { class: "media", role: "img", "aria-label": m.alt || "Image without alt text", style: `aspect-ratio:${ratio(m)}` },
      `Image ${m.natural_w || "?"} x ${m.natural_h || "?"} px${m.alt ? "" : " (no alt text)"}`);
  }

  function optionList(q) {
    const hidden = q.options_below_fold || 0, items = [];
    q.options.forEach((o, i) => {
      if (hidden && i === q.options.length - hidden) items.push(h("li", { class: "fold" }, "Below the fold on a phone"));
      items.push(h("li", null, o.media ? mediaBox(o.media) : null, o.label));
    });
    return h("ul", { class: q.options.some((o) => o.media) ? "opts grid-opts" : "opts" }, items);
  }

  function questionBody(q) {
    const scale = q.scale;
    switch (q.kind) {
      case "dropdown": return h("div", { class: "dropdown" }, h("span", null, "Select one"), h("span", null, `${q.options.length} choices`));
      case "text_short": case "text_long": return h("div", { class: "textbox" }, "Type your answer here");
      case "rating": case "slider": return [h("div", { class: "scale" }, points(scale).map((n) => h("span", null, String(n)))),
        h("div", { class: "ends" }, h("span", null, scale.low_label || "(no label)"), h("span", null, scale.high_label || "(no label)"))];
      case "grid_single": case "grid_multi": return h("table", null, h("caption", null, `${scale.low_label || ""} to ${scale.high_label || ""}`),
        h("thead", null, h("tr", null, h("td", null), points(scale).map((n) => h("th", { scope: "col" }, String(n))))),
        h("tbody", null, q.rows.map((r) => h("tr", null, h("th", { scope: "row" }, r), points(scale).map(() => h("td", null, h("span", { class: "dot" })))))));
      default: return optionList(q);
    }
  }

  function renderQuestion(q, flags, selectedId) {
    const cls = ["q", flags && "flagged", flags && flags.must && "has-must", q.id === selectedId && "selected", q.kind === "multi_choice" && "multi"].filter(Boolean).join(" ");
    return h("div", { class: cls },
      flags && h("p", { class: "flag-note" }, `Coach flagged this question (${flags.count})`),
      (q.media || []).map(mediaBox),
      h("p", { class: "q-text" }, q.text), q.help_text && h("p", { class: "help" }, q.help_text),
      questionBody(q), q.required === false && h("p", { class: "help" }, "Optional"));
  }

  function renderPage(page, flagsByQuestion, selectedId) {
    if (page.kind === "intro") return [h("h3", null, "Welcome"), h("p", null, page.intro_text), h("div", { class: "next" }, "Start")];
    if (page.kind !== "question") return h("div", { class: "centered" }, h("p", null, page.text));
    return [(page.questions || []).map((q) => renderQuestion(q, flagsByQuestion[q.id], selectedId)), h("div", { class: "next" }, "Next")];
  }

  function renderPhone() {
    const { review, snapshot } = current(), pages = snapshot.pages, page = pages[state.page];
    const flags = {};
    review.findings.forEach((f) => { if (f.question_id) { const e = flags[f.question_id] || (flags[f.question_id] = { count: 0, must: false }); e.count++; e.must ||= f.severity === "must_fix"; } });
    const selected = state.selected == null ? null : review.findings[state.selected].question_id;
    mount($("phone-panel"), 
      h("h2", { id: "phone-h" }, "Phone preview"),
      h("p", { class: "note" }, "A simple picture of what a member sees. Flagged questions are outlined and labeled."),
      h("div", { class: "phone" },
        h("div", { class: "phone-bar" }, h("span", null, `Screen ${state.page + 1} of ${pages.length}`), h("span", null, page.kind === "question" ? "Question" : page.kind.replace("_", " "))),
        h("div", { class: "phone-screen", tabindex: "0", role: "region", "aria-label": "Survey screen preview, scrollable" }, renderPage(page, flags, selected))),
      h("div", { class: "pager" },
        h("button", { type: "button", disabled: state.page === 0, onclick: () => goTo(state.page - 1) }, "Previous screen"),
        h("button", { type: "button", disabled: state.page === pages.length - 1, onclick: () => goTo(state.page + 1) }, "Next screen")),
      state.selected != null && h("p", null, h("button", { type: "button", class: "linkish", onclick: backToFinding }, "Back to the selected finding")));
  }

  function goTo(n) {
    state.page = n;
    renderPhone();
    const next = document.querySelector(".pager button:not(:disabled)");
    (n === 0 ? document.querySelectorAll(".pager button")[1] : n === current().snapshot.pages.length - 1 ? document.querySelectorAll(".pager button")[0] : next).focus();
  }

  /* ---------- picker and boot ---------- */
  function renderPicker() {
    $("picker").replaceChildren(...DATA.surveys.map((s, i) =>
      h("label", null, h("input", { type: "radio", name: "survey", value: i, checked: i === state.survey, onchange: () => chooseSurvey(i) }), h("span", null, s.title))));
  }

  function chooseSurvey(i) {
    Object.assign(state, { survey: i, filter: "all", selected: null, page: 0 });
    renderAll();
    say(`Showing the sample survey: ${current().title}. Readiness: ${READINESS[current().review.scorecard.readiness]}.`);
  }

  function renderAll() {
    $("blurb").textContent = current().blurb;
    renderSummary(); renderFindings(); renderPhone();
  }

  $("disclaimer").textContent = DATA.disclaimer;
  renderPicker();
  renderAll();
})();
