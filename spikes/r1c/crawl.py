"""Spike R1c: generic survey crawler prototype (OBSERVE -> PLAN -> ACT -> VERIFY).

Approved by Onder for testing on posthalloween26. Creates one tagged test participant.
Usage: python crawl.py <url> [max_pages] [--allow-submit]
"""
import hashlib
import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent.parent / "r1b"))
from record import Recorder  # noqa: E402  (spike reuse of the redacting recorder)
from definition import EXCLUSIVE, Definition, norm  # noqa: E402

OUT = Path(__file__).parent / time.strftime("run-%H%M%S")
PROXY = {"server": "http://proxy-intlho.wal-mart.com:8080"}
PHONE = {
    "viewport": {"width": 393, "height": 852}, "device_scale_factor": 3,
    "is_mobile": True, "has_touch": True, "locale": "en-US",
    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 "
                  "(KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
}
ADVANCE = re.compile(r"^\s*(next|continue|begin|start|submit|finish|done|ok|>|›|→)\s*$", re.I)
FINAL = re.compile(r"^\s*(submit|finish|done)\s*$", re.I)
TEST_TEXT = "SurveyCoach test"

# One pass in the page: tag interactive elements, group them, report everything as data.
OBSERVE_JS = r"""() => {
  const visible = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
    return r.width > 2 && r.height > 2 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const label = e => (e.getAttribute('aria-label') || e.innerText || e.value || e.placeholder
    || (e.labels && e.labels[0] && e.labels[0].innerText) || '').trim().replace(/\s+/g, ' ').slice(0, 120);
  let n = 0;
  const sel = 'input, select, textarea, button, a[href], [role=radio], [role=checkbox], [role=button],'
    + '[role=slider], [role=option], [role=switch], [contenteditable=true], [tabindex="0"]';
  const els = [...document.querySelectorAll(sel)].filter(visible);
  const isAdvance = e => /^\s*(next|continue|begin|start|submit|finish|done|ok)\s*$/i.test(e.innerText || e.value || '');
  const answerEls = els.filter(e => !isAdvance(e));
  // Group = nearest ancestor holding at least two answer controls (list for buttons, row for matrices).
  const groupOf = e => { let a = e.parentElement;
    while (a && a !== document.body && answerEls.filter(x => a.contains(x)).length < 2) a = a.parentElement;
    if (!a.dataset.scGroup) a.dataset.scGroup = 'g' + (++n); return a.dataset.scGroup; };
  const items = els.map(e => {
    const id = e.dataset.scId || ('sc' + (++n) + '_' + Math.random().toString(36).slice(2, 6));
    e.dataset.scId = id;
    const r = e.getBoundingClientRect();
    return { id, tag: e.tagName.toLowerCase(), type: (e.type || '').toLowerCase(),
      role: e.getAttribute('role') || '', name: e.name || '', label: label(e),
      checked: !!(e.checked || e.getAttribute('aria-checked') === 'true' || e.getAttribute('aria-pressed') === 'true'),
      min: e.min || e.getAttribute('aria-valuemin') || '', max: e.max || e.getAttribute('aria-valuemax') || '',
      group: e.name || groupOf(e), cls: (e.className && e.className.baseVal === undefined ? e.className : '').slice(0, 80),
      box: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)] };
  });
  const scrollers = [...document.querySelectorAll('*')].filter(e => e.scrollHeight > e.clientHeight + 4
    && /(auto|scroll)/.test(getComputedStyle(e).overflowY));
  const main = scrollers.sort((a, b) => b.clientHeight - a.clientHeight)[0] || document.scrollingElement;
  const text = (document.body.innerText || '').replace(/\s+/g, ' ').trim();
  const errors = [...document.querySelectorAll('[class*=error], [role=alert], .text-danger, .invalid-feedback')]
    .filter(visible).map(e => e.innerText.trim()).filter(Boolean).slice(0, 5);
  const imgs = [...document.images].filter(visible).map(i => ({ src: i.currentSrc, natural: [i.naturalWidth, i.naturalHeight],
    rendered: [Math.round(i.getBoundingClientRect().width), Math.round(i.getBoundingClientRect().height)],
    fit: getComputedStyle(i).objectFit, alt: i.alt }));
  return { url: location.href, text: text.slice(0, 3000), items, errors, images: imgs,
           scroller: { height: main.scrollHeight, client: main.clientHeight } };
}"""


def fingerprint(obs: dict) -> str:
    return hashlib.sha1((obs["url"] + obs["text"][:1500]).encode()).hexdigest()[:12]


def split(obs: dict):
    """Separate the advance control from answer groups."""
    advance = [i for i in obs["items"] if ADVANCE.match(i["label"]) and i["tag"] in ("button", "a", "input")]
    answers = [i for i in obs["items"] if i not in advance and i["tag"] != "a"]
    groups: dict[str, list] = {}
    for item in answers:
        groups.setdefault(item["group"], []).append(item)
    return (advance[-1] if advance else None), groups


def kind_of(group: list) -> str:
    first = group[0]
    if first["tag"] == "textarea" or first["type"] in ("text", "email", "search", "") and first["tag"] == "input":
        return "text"
    if first["type"] == "number" or first["role"] == "spinbutton":
        return "numeric"
    if first["tag"] == "select":
        return "dropdown"
    if first["type"] == "range" or first["role"] == "slider":
        return "slider"
    if first["type"] == "checkbox" or first["role"] == "checkbox":
        return "multi_choice"
    if first["type"] == "radio" or first["role"] == "radio" or len(group) >= 2:
        return "single_choice"
    return "unknown"


def below_fold(groups: dict, advance: dict | None) -> int:
    """Answer controls that end below the top of the advance button (platform-neutral fold)."""
    if not advance:
        return 0
    fold = advance["box"][1]
    return sum(1 for g in groups.values() for i in g if i["box"][1] + i["box"][3] > fold)


def plan(groups: dict, chosen: list[str] | None = None) -> list[tuple]:
    """Definition picks (by label) when available; generic strategies otherwise."""
    actions = []
    wanted = {norm(c) for c in chosen or []}
    for gid, group in groups.items():
        kind = kind_of(group)
        if kind in ("single_choice", "multi_choice"):
            if any(i["checked"] for i in group):
                continue
            matches = [i for i in group if norm(i["label"]) in wanted]
            if matches:
                actions += [("definition", "click", i["id"], None) for i in matches]
                continue
            if wanted:
                continue  # the definition already decided this page's choices
            pool = [i for i in group if not EXCLUSIVE.search(i["label"])] or group
            actions.append((kind, "click", pool[0]["id"], None))
        elif kind == "text":
            for i in group:
                actions.append((kind, "fill", i["id"], TEST_TEXT))
        elif kind == "numeric":
            for i in group:
                lo, hi = float(i["min"] or 1), float(i["max"] or 10)
                actions.append((kind, "fill", i["id"], str(int((lo + hi) // 2))))
        elif kind == "dropdown":
            actions.append((kind, "select", group[0]["id"], None))
        elif kind == "slider":
            actions.append((kind, "keys", group[0]["id"], None))
    return actions


def act(page, actions: list[tuple]) -> None:
    for kind, verb, el_id, value in actions:
        loc = page.locator(f'[data-sc-id="{el_id}"]')
        try:
            if verb == "click":
                loc.scroll_into_view_if_needed(timeout=3000)
                loc.click(timeout=5000)
            elif verb == "fill":
                loc.fill(value, timeout=5000)
            elif verb == "select":
                loc.select_option(index=1, timeout=5000)
            elif verb == "keys":
                loc.focus()
                for _ in range(5):
                    loc.press("ArrowRight")
            page.wait_for_timeout(300)
        except Exception as exc:  # spike: log and continue
            print(f"    ! {verb} {kind} {el_id}: {str(exc)[:100]}")


def save(page, n: int, obs: dict, tag: str = "") -> None:
    page.screenshot(path=str(OUT / f"p{n:02d}{tag}-viewport.png"))
    (OUT / f"p{n:02d}{tag}.html").write_text(page.content())
    (OUT / f"p{n:02d}{tag}-aria.yaml").write_text(page.locator("body").aria_snapshot())
    (OUT / f"p{n:02d}{tag}-obs.json").write_text(json.dumps(obs, indent=1))


def crawl(url: str, max_pages: int, allow_submit: bool) -> None:
    OUT.mkdir(parents=True)
    recorder = Recorder(str(OUT / "api"))
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True, proxy=PROXY)
        context = browser.new_context(**PHONE)
        recorder.attach(context)
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.locator("button:visible, input:visible").first.wait_for(timeout=30000)
        page.wait_for_timeout(4000)
        seen, stop, selected, visited = {}, "max pages", set(), set()
        for n in range(max_pages):
            obs = page.evaluate(OBSERVE_JS)
            fp = fingerprint(obs)
            save(page, n, obs)
            advance, groups = split(obs)
            seen[fp] = seen.get(fp, 0) + 1
            definition = Definition.find_in(OUT / "api-bodies")
            def_page = definition.page_for(obs["text"]) if definition else None
            chosen = definition.choose(def_page) if def_page else None
            print(f"\n[p{n:02d}] fp={fp} {obs['text'][:110]!r}")
            print(f"  groups: {[(kind_of(g), len(g), g[0]['label'][:25]) for g in groups.values()][:8]}")
            print(f"  advance: {advance and advance['label']!r}  images: {len(obs['images'])}"
                  f"  below fold: {below_fold(groups, advance)}")
            print(f"  definition page: {def_page and def_page['index']}  chosen: {chosen}")
            if def_page:
                visited.add(def_page["index"])
            if seen[fp] > 3:
                stop = "loop: same page 3 times"
                break
            if not advance:
                stop = "no advance control (end, screen-out, or unknown widget)"
                break
            if chosen:
                selected |= definition.ids_for(chosen)
            final = (def_page and definition.is_last(def_page, selected)) or FINAL.match(advance["label"])
            if final and n > 0 and not allow_submit:
                stop = f"final-submit stop before advancing page {n} ({advance['label']})"
                break
            for attempt in range(3):
                actions = plan(groups, chosen)
                print(f"  plan#{attempt}: {[(a[0], a[1]) for a in actions]}")
                act(page, actions)
                page.locator(f'[data-sc-id="{advance["id"]}"]').click(timeout=5000)
                page.wait_for_timeout(2500)
                after = page.evaluate(OBSERVE_JS)
                if fingerprint(after) != fp:
                    break
                print(f"  ! page unchanged; errors: {after['errors']}")
                save(page, n, after, f"-retry{attempt}")
                advance, groups = split(after)
                if not advance:
                    break
            else:
                stop = f"blocked at page {n}"
                break
        print(f"\nSTOP: {stop}\nartifacts: {OUT}")
        definition = Definition.find_in(OUT / "api-bodies")
        if definition:
            print(f"definition captured: {len(definition.pages)} pages; walked {sorted(visited)}")
            print(definition.summary())
        browser.close()
    calls = [json.loads(line) for line in Path(f"{OUT}/api-network.jsonl").open()] \
        if Path(f"{OUT}/api-network.jsonl").exists() else []
    print(f"api calls: {len(calls)}")
    for c in calls:
        print(f"  {c['method']} {c['status']} {c['url'][29:120]} {c.get('body_bytes')}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    crawl(args[0], int(args[1]) if len(args) > 1 else 60, "--allow-submit" in sys.argv)
