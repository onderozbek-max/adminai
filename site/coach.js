(() => {
  "use strict";
  const SC = window.SC;
  const { h, plural } = SC;

  function chips(entry, ctx) {
    const { f, n } = entry, criterion = ctx.data.criteria[f.criterion_id] || {};
    const area = ctx.data.dimensions[criterion.dimension];   // blockers have no area; "Must fix" already says it
    return h("div", { class: "chips" },
      h("span", { class: "badge-n" }, String(n)),
      h("span", { class: `chip ${f.severity}` }, SC.SEVERITY[f.severity]),
      area && h("span", { class: "chip area" }, area),
      ctx.applied(entry) && h("span", { class: "chip good" }, "Fixed in preview"));
  }

  /** Word-level before/after: only the words that change are marked, so nobody has to compare two sentences. */
  function diffParts(before, after) {
    const a = before.split(" "), b = after.split(" ");
    let head = 0;
    while (head < a.length && head < b.length && a[head] === b[head]) head += 1;
    let tail = 0;
    while (tail < a.length - head && tail < b.length - head && a[a.length - 1 - tail] === b[b.length - 1 - tail]) tail += 1;
    const join = (words) => words.join(" ");
    return { head: join(a.slice(0, head)), cut: join(a.slice(head, a.length - tail)), add: join(b.slice(head, b.length - tail)), tail: join(a.slice(a.length - tail)) };
  }

  const spaced = (...parts) => parts.filter(Boolean).flatMap((p, i) => (i ? [" ", p] : [p]));

  /** "Which version is better?": the researcher's pick drives the phone preview and what gets copied. */
  function choiceBlock(entry, ctx) {
    const { f, key, n } = entry, picked = ctx.choiceOf(key), msg = h("p", { class: "note", role: "status" });
    const d = f.current_text ? diffParts(f.current_text, f.suggested_text) : null;
    const radio = (value, label, text) => h("label", { class: `opt${picked === value ? " on" : ""}` },
      h("input", { type: "radio", name: `choice-${key}`, value, checked: picked === value, "data-fk": `opt-${key}-${value}`, onchange: () => ctx.onChoose(key, value) }),
      h("span", { class: "opt-body" }, h("span", { class: "opt-label" }, label), h("span", { class: "opt-text" }, text)));
    return h("fieldset", { class: "choice" },
      h("legend", null, "Which version is better?"),
      radio("original", f.current_text ? "Your original" : "Leave as is",
        d ? spaced(d.head, d.cut && h("del", null, d.cut), d.tail) : "Nothing added"),
      radio("suggested", "Suggested", d ? spaced(d.head, d.add && h("ins", null, d.add), d.tail) : f.suggested_text),
      h("div", { class: "actions" },
        h("button", { type: "button", class: "btn", "data-fk": `copy-${key}`, "aria-label": `Copy suggested text for issue ${n}`, onclick: () => ctx.onCopy(f.suggested_text, msg) }, "Copy suggested text"),
        h("span", { class: "note" }, picked === "suggested" ? "Shown on the phone under With fixes." : "Your original stays in the preview.")),
      msg);
  }

  function card(entry, ctx) {
    const { f, key } = entry, selected = ctx.selected === key;
    return h("article", { class: `card ${f.severity}${selected ? " selected" : ""}`, id: `card-${key}` },
      chips(entry, ctx),
      h("h3", null, h("button", { type: "button", class: "card-head", "data-fk": `card-${key}`, "aria-pressed": String(selected), onclick: () => ctx.onSelect(key) }, f.headline)),
      h("p", { class: "why" }, f.member_impact),
      h("p", { class: "fix" }, h("strong", null, "How to fix: "), f.explanation),
      f.suggested_text ? choiceBlock(entry, ctx) : null);
  }

  function areaRow(id, d, ctx) {
    const unchecked = Object.values(ctx.data.criteria)
      .filter((c) => c.dimension === id && ctx.review.unchecked.includes(c.title)).reduce((sum, c) => sum + c.points, 0);
    const checked = d.possible - unchecked, earned = d.earned - unchecked, pct = (x) => `${(x / d.possible) * 100}%`;
    return h("li", null, h("span", null, d.name),
      h("span", { class: "bar", "aria-hidden": "true" },
        h("i", { class: "got", style: `width:${pct(earned)}` }), h("i", { class: "lost", style: `width:${pct(checked - earned)}` }),
        h("i", { class: "wait", style: `width:${pct(unchecked)}` })),
      h("span", { class: "num" }, checked ? `${earned.toFixed(1)} of ${checked} checked` : "Not checked yet", unchecked && checked ? `, ${unchecked} waiting` : ""));
  }

  function report(ctx) {
    const { scorecard, unchecked } = ctx.review;
    return h("section", { class: "report", "aria-labelledby": "report-h" },
      h("h2", { id: "report-h" }, "Report"),
      h("details", null, h("summary", null, "Score by area"),
        h("ul", { class: "areas" }, Object.entries(scorecard.by_dimension).map(([id, d]) => areaRow(id, d, ctx))),
        h("p", { class: "legend" }, h("i", { class: "got" }), " earned ", h("i", { class: "lost" }), " lost ", h("i", { class: "wait" }), " not checked yet")),
      h("details", null, h("summary", null, `Waiting on the AI step (${plural(unchecked.length, "check")})`),
        h("ul", { class: "plain" }, unchecked.map((title) => h("li", null, title)))),
      h("details", null, h("summary", null, "What is working"),
        h("ul", { class: "plain" }, (scorecard.strengths.length ? scorecard.strengths : ["Nothing confirmed yet."]).map((s) => h("li", null, s)))));
  }

  SC.renderCoach = (item, ctx) => {
    const n = item.entries.length;
    const sub = n
      ? `${plural(n, "thing")} to look at ${item.page ? "on this screen" : "across the whole survey"}.`
      : "No issues found here. The AI step has not run yet, so tone and leading wording are not checked.";
    return [h("h2", { id: "coach-h" }, "Coach"), h("p", { class: "sub" }, sub), item.entries.map((e) => card(e, ctx)), report(ctx)];
  };
})();
