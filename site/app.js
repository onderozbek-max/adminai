(() => {
  "use strict";
  const SC = window.SC, { h, mount, $, say, plural, clock } = SC;
  const DATA = window.SURVEYCOACH_DEMO;
  const DEVICES = [["iPhone SE", 320], ["iPhone 16", 390], ["Android XL", 412]];
  const TONE = { needs_work: "red", almost_ready: "amber", ready: "green" };
  const state = { survey: 0, screen: 0, mode: "current", device: 390, large: false, selected: null, choices: {} };
  let model;

  const survey = () => DATA.surveys[state.survey];
  const current = () => model.order[state.screen];
  const pageItem = () => (current().page ? current() : model.items[0]);
  const choiceOf = (key) => state.choices[`${state.survey}:${key}`] || "suggested";
  const applied = (entry) => state.mode === "fixes" && !!entry.f.suggested_text && choiceOf(entry.key) === "suggested";

  /** current text -> chosen suggestion, so the phone can show the survey as it would read after the fixes. */
  function fixMap() {
    if (state.mode !== "fixes") return null;
    const map = {};
    survey().review.findings.forEach((f, key) => {
      if (f.current_text && f.suggested_text && choiceOf(key) === "suggested") map[f.current_text] = f.suggested_text;
    });
    return map;
  }

  async function copy(text, msg) {
    try {
      await navigator.clipboard.writeText(text);
      msg.textContent = "Copied. Paste it into RedJade yourself: SurveyCoach does not change your survey.";
    } catch (_) {
      msg.textContent = "Copy is not available in this browser. Select the suggested text and copy it.";
    }
  }

  function scrollPhoneTo(key) {
    const pinEl = document.querySelector(`.phone-screen [data-pin="${key}"]`), screen = document.querySelector(".phone-screen");
    if (!pinEl || !screen) return;
    const s = screen.getBoundingClientRect(), p = pinEl.getBoundingClientRect();
    screen.scrollTop += p.top - s.top - s.height / 3;   // scroll the phone only, never the page
  }

  function select(key, focusCard) {
    state.screen = Math.max(0, model.order.findIndex((item) => item.entries.some((e) => e.key === key)));
    state.selected = key;
    renderAll();
    scrollPhoneTo(key);
    if (focusCard) {
      const head = document.querySelector(`[data-fk="card-${key}"]`);
      head.focus();
      head.scrollIntoView({ block: "nearest" });
    }
  }

  function goToScreen(i) {
    state.screen = i;
    state.selected = current().entries.length ? current().entries[0].key : null;
    renderAll();
  }

  const context = () => ({
    data: DATA, review: survey().review, selected: state.selected, device: state.device, large: state.large,
    total: model.items.length, fixes: fixMap(), applied, choiceOf,
    onPin: (key) => select(key, true), onSelect: (key) => select(key, false),
    onChoose: (key, value) => { state.choices[`${state.survey}:${key}`] = value; renderAll(); },
    onCopy: copy,
  });

  /* ---------- header ---------- */
  const stat = (value, label, tone) => h("div", { class: `stat ${tone}` }, h("dd", null, String(value)), h("dt", null, label));

  function headline(review) {
    const { readiness, open_blockers } = review.scorecard;
    const must = review.findings.filter((f) => f.severity === "must_fix").length, worth = review.findings.length - must;
    if (readiness === "needs_work") return `Needs work. Fix ${plural(open_blockers.length || must, "thing")} first.`;
    if (readiness === "ready") return "Ready to launch.";
    return worth ? `Almost ready. ${plural(worth, "improvement")} to consider.` : "Nothing to fix yet. The AI step still has to run.";
  }

  function renderTop() {
    const { review } = survey(), card = review.scorecard;
    const checked = 100 - card.unchecked_points, earned = card.score - card.unchecked_points;
    const must = review.findings.filter((f) => f.severity === "must_fix").length, worth = review.findings.length - must;
    const promised = review.promised_minutes ? `intro promises ${review.promised_minutes}` : "";
    const waiting = `${card.unchecked_points} points${card.pending_blockers.length ? ` and ${plural(card.pending_blockers.length, "launch check")}` : ""} wait on the AI step`;
    // The ring shows all 100 points: earned, lost, and not checked yet. Unchecked points are never drawn as earned.
    mount($("topbar"),
      h("div", { class: "brand" }, "Survey", h("span", null, "Coach")),
      h("div", { class: "ring-block" },
        h("div", { class: `ring ${TONE[card.readiness]}`, role: "img", style: `--e:${earned * 3.6}deg;--k:${checked * 3.6}deg`,
          "aria-label": `${earned.toFixed(0)} of the ${checked} points checked so far were earned. ${waiting}.` },
        h("div", { class: "ring-in" }, earned.toFixed(0))),
        h("span", { class: "ring-cap" }, `of ${checked} checked`)),
      h("div", { class: "head-text" },
        h("h1", null, headline(review)),
        h("p", { class: "sub" }, `${survey().title} \u2022 ${waiting}`),
        h("p", { class: "brief" }, `${must} must fix \u2022 ${worth} worth improving \u2022 ${review.est_minutes} min \u2022 AI check pending`)),
      h("dl", { class: "stats" }, stat(must, "must fix", "red"), stat(worth, "worth improving", "amber"),
        stat(`${review.est_minutes} min`, promised ? `for members, ${promised}` : "for members", "plain")),
      h("label", { class: "pick" }, h("span", null, "Sample survey"),
        h("select", { "data-fk": "survey-picker", onchange: (e) => chooseSurvey(Number(e.target.value)) },
          DATA.surveys.map((s, i) => h("option", { value: i, selected: i === state.survey }, s.title)))));
  }

  /* ---------- rail ---------- */
  function railItem(item, i) {
    const on = i === state.screen, n = item.entries.length;
    return h("button", { type: "button", class: `rail-item${on ? " on" : ""}`, "data-fk": `rail-${i}`, "aria-current": on ? "true" : false, onclick: () => goToScreen(i) },
      h("span", { class: `dot ${item.worst || "ok"}`, "aria-hidden": "true" }),
      h("span", { class: "rail-text" },
        h("strong", { class: "line1" }, item.name, item.topic && h("span", { class: "topic" }, ` ${item.topic}`)),
        h("span", { class: `issue ${item.worst || "ok"}` }, n ? item.entries[0].f.headline : "Nothing flagged yet")),
      n > 1 && h("span", { class: "count", "aria-label": plural(n, "issue") }, String(n)));
  }

  /* ---------- stage ---------- */
  const seg = (label, options, value, onPick, prefix) =>
    h("div", { class: "seg", role: "group", "aria-label": label },
      options.map(([v, text]) => h("button", { type: "button", "aria-pressed": String(v === value), "data-fk": `${prefix}-${v}`, onclick: () => onPick(v) }, text)));

  function goToPage(index) {
    state.screen = model.order.indexOf(model.items[index]);
    state.selected = current().entries.length ? current().entries[0].key : null;
    renderAll();
  }

  /** One line above the phone (phones only): what is wrong on this screen, without scrolling to the coach. */
  function leadLine() {
    const entry = current().entries.find((e) => e.key === state.selected);
    if (!entry) return null;
    return h("button", { type: "button", class: `lead ${entry.f.severity}`, "data-fk": "lead", onclick: () => {
      const head = document.querySelector(`[data-fk="card-${entry.key}"]`);
      head.focus(); head.scrollIntoView({ block: "center" });
    } }, h("span", { class: "badge-n" }, String(entry.n)), h("span", null, entry.f.headline), h("span", { class: "more" }, "Details"));
  }

  function renderStage() {
    const item = pageItem(), s = survey(), seconds = s.timeline[item.index].seconds;
    mount($("stage"),
      h("h2", { id: "stage-h", class: "sr-only" }, "Phone preview"),
      h("div", { class: "toolbar" },
        seg("View", [["current", "Current"], ["fixes", "With fixes"]], state.mode, (v) => { state.mode = v; renderAll(); say(v === "fixes" ? "Showing the survey with your chosen fixes." : "Showing the survey as it is now."); }, "mode"),
        seg("Device", DEVICES.map(([name, w]) => [String(w), name]), String(state.device), (v) => { state.device = Number(v); renderAll(); }, "dev"),
        h("button", { type: "button", class: "toggle", "aria-pressed": String(state.large), "data-fk": "large", onclick: () => { state.large = !state.large; renderAll(); } }, "Large text")),
      leadLine(),
      SC.renderPhone(item, context()),
      h("div", { class: "pager" },
        h("button", { type: "button", "data-fk": "prev", disabled: item.index === 0, onclick: () => goToPage(item.index - 1) }, "Previous screen"),
        h("button", { type: "button", "data-fk": "next", disabled: item.index === model.items.length - 1, onclick: () => goToPage(item.index + 1) }, "Next screen")),
      h("div", { class: "timing" },
        h("p", null, `Members reach this screen at about ${clock(seconds)} of ${clock(s.total_seconds)}.`),
        h("div", { class: "timebar", "aria-hidden": "true" }, h("i", { style: `left:${(seconds / s.total_seconds) * 100}%` }))));
  }

  /* ---------- boot ---------- */
  function restoreFocus(key) {
    if (!key) return;
    const target = document.querySelector(`[data-fk="${key}"]`);
    const usable = target && !target.disabled ? target : $("stage").querySelector(".pager button:not(:disabled)");
    if (usable) usable.focus({ preventScroll: true });
  }

  function centerSelectedInRail() {   // scroll the rail strip only, never the page
    const rail = $("rail"), on = rail.querySelector(".rail-item.on");
    if (!on) return;
    if (rail.scrollWidth > rail.clientWidth && getComputedStyle(rail).flexDirection === "row") {
      rail.scrollLeft = on.offsetLeft - (rail.clientWidth - on.offsetWidth) / 2;
    } else if (rail.scrollHeight > rail.clientHeight) {
      rail.scrollTop = on.offsetTop - (rail.clientHeight - on.offsetHeight) / 2;
    }
  }

  let lastPage = null;
  function renderAll() {
    const active = document.activeElement, key = active && active.dataset ? active.dataset.fk : null;
    const before = document.querySelector(".phone-screen"), keepTop = before ? before.scrollTop : 0;
    const pageKey = `${state.survey}:${pageItem().index}`, samePage = pageKey === lastPage;
    lastPage = pageKey;
    renderTop();
    mount($("strip"), h("span", { class: "long" }, DATA.disclaimer), h("span", { class: "short" }, DATA.disclaimer_short));
    mount($("rail"), h("h2", { class: "sr-only" }, "Screens"), model.order.map(railItem));
    renderStage();
    mount($("coach"), SC.renderCoach(current(), context()));
    centerSelectedInRail();
    if (samePage) document.querySelector(".phone-screen").scrollTop = keepTop;
    else if (state.selected != null) scrollPhoneTo(state.selected);
    restoreFocus(key);
  }

  function chooseSurvey(i) {
    state.survey = i;
    model = SC.buildModel(survey());
    state.mode = "current";
    state.screen = model.order.indexOf(model.start);
    state.selected = model.start.entries.length ? model.start.entries[0].key : null;
    renderAll();
    say(`Showing the sample survey: ${survey().title}. ${SC.READINESS[survey().review.scorecard.readiness]}.`);
  }

  chooseSurvey(0);
})();
