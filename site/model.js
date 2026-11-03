(() => {
  "use strict";
  const SC = window.SC;
  const RANK = { must_fix: 0, worth_improving: 1 };
  SC.SPLIT = " ... ";   // joins a scale's two end labels into one fixable string

  /** The versions a researcher can pick between: the AI's options, or the single code-made suggestion. */
  SC.choicesOf = (f) => (f.options && f.options.length
    ? f.options.map((o, i) => ({ value: String(i), label: o.label, text: o.text }))
    : f.suggested_text ? [{ value: "suggested", label: "Suggested", text: f.suggested_text }] : []);

  /** null means "keep the original". With no pick yet, the first (recommended) version is chosen. */
  SC.chosenChoice = (f, value) => {
    if (value === "original") return null;
    const list = SC.choicesOf(f);
    return list.find((c) => c.value === value) || list[0] || null;
  };

  /** Apply the chosen fixes to one string, first fix wins. `hits` collects the fixes that really changed something. */
  SC.applyFixes = (text, plan, hits) => plan.reduce((t, fix) => {
    if (!t.includes(fix.from)) return t;
    if (hits) hits.add(fix.key);
    return t.replace(fix.from, fix.to);
  }, text);

  /** Every string the phone shows through the fixer for this page, so "fixed in preview" can be checked, not assumed. */
  SC.pageTexts = (page) => [page.intro_text, page.text, ...(page.questions || []).flatMap((q) => [
    q.text, q.help_text, ...q.options.map((o) => o.label),
    q.scale && `${q.scale.low_label || "(no label)"}${SC.SPLIT}${q.scale.high_label || "(no label)"}`]),
  ].filter(Boolean);

  SC.hitsOn = (page, plan) => {
    const hits = new Set();
    SC.pageTexts(page).forEach((text) => SC.applyFixes(text, plan, hits));
    return hits;
  };

  /** Which findings belong to which screen, numbered the way the phone pins and the coach cards will show them. */
  SC.buildModel = function buildModel(survey) {
    const { snapshot, review } = survey;
    for (const page of snapshot.pages) {   // exported snapshots omit empty lists; normalize once
      page.questions = page.questions || [];
      for (const q of page.questions) Object.assign(q, { options: q.options || [], rows: q.rows || [], media: q.media || [] });
    }
    const pageIndex = new Map(snapshot.pages.map((page, i) => [page.id, i]));
    const questionPage = new Map();
    snapshot.pages.forEach((page, i) => (page.questions || []).forEach((q) => questionPage.set(q.id, i)));
    const locate = (f) => questionPage.get(f.question_id) ?? pageIndex.get(f.page_id) ?? -1;

    let questionNumber = 0;
    const items = snapshot.pages.map((page, index) => {
      const first = (page.questions || [])[0];
      if (page.kind === "question") questionNumber += 1;
      const name = { intro: "Intro", thank_you: "Thank you", screen_out: "Screen-out" }[page.kind] || `Q${questionNumber}`;
      return { index, page, name, topic: first ? SC.clip(first.text, 34) : "", entries: [] };
    });
    const whole = { index: -1, page: null, name: "Whole survey", topic: "Applies to every screen", entries: [] };

    review.findings.forEach((f, key) => (items[locate(f)] || whole).entries.push({ f, key }));
    for (const item of [...items, whole]) {
      item.entries.sort((a, b) => RANK[a.f.severity] - RANK[b.f.severity] || a.key - b.key);
      item.entries.forEach((entry, i) => { entry.n = i + 1; });
      item.worst = item.entries.length ? item.entries[0].f.severity : null;
    }

    const order = whole.entries.length ? [whole, ...items] : items;
    const start = order.find((it) => it.worst === "must_fix") || order.find((it) => it.entries.length) || order[0];
    return { items, whole, order, start };
  };
})();
