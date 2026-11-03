"""Spike R1b: render the RedJade previewer as an iPhone 16 and step through pages.

Read-only intent: previewer demo mode only. Logs any POST so we can prove nothing is saved.
Usage: python mobile.py <label> <project_id> <pages>
"""
import json
import re
import sys

from playwright.sync_api import sync_playwright

from preview import open_previewer
from record import OUT, Recorder

IPHONE_16 = {"width": 393, "height": 852, "deviceScaleFactor": 3, "mobile": True}
IPHONE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
)
NEXT_LABEL = re.compile(r"^\s*next\s*$", re.I)

GEOMETRY_JS = """() => {
  const vw = window.innerWidth, vh = window.innerHeight;
  const doc = document.scrollingElement || document.documentElement;
  const imgs = [...document.images].map(i => ({src: i.currentSrc.slice(-60), natural: [i.naturalWidth, i.naturalHeight],
      rendered: [Math.round(i.getBoundingClientRect().width), Math.round(i.getBoundingClientRect().height)],
      fit: getComputedStyle(i).objectFit, alt: i.alt}));
  const overflowX = [...document.querySelectorAll('body *')].filter(e => e.scrollWidth > e.clientWidth + 2
      && getComputedStyle(e).overflowX !== 'visible').length;
  const q = document.querySelector('p, h1, h2, h3, label');
  return {viewport: [vw, vh], scrollHeight: doc.scrollHeight, fitsOneScreen: doc.scrollHeight <= vh,
          horizontalScrollers: overflowX, images: imgs,
          firstTextFont: q ? getComputedStyle(q).fontFamily + ' ' + getComputedStyle(q).fontSize : null};
}"""


def emulate_phone(page) -> None:
    cdp = page.context.new_cdp_session(page)
    cdp.send("Emulation.setDeviceMetricsOverride", IPHONE_16)
    cdp.send("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
    cdp.send("Network.setUserAgentOverride", {"userAgent": IPHONE_UA})


def main(label: str, project_id: str, page_count: int) -> None:
    recorder = Recorder(label)
    with sync_playwright() as p:
        context = p.chromium.connect_over_cdp("http://127.0.0.1:9223").contexts[0]
        recorder.attach(context)
        page = open_previewer(context, project_id)
        emulate_phone(page)
        page.reload()
        page.wait_for_timeout(5000)
        for n in range(page_count):
            page.screenshot(path=str(OUT / f"{label}-p{n:02d}-viewport.png"))
            page.screenshot(path=str(OUT / f"{label}-p{n:02d}-full.png"), full_page=True)
            print(f"page {n}:", json.dumps(page.evaluate(GEOMETRY_JS))[:400])
            next_button = page.get_by_role("button", name=NEXT_LABEL).first
            if not next_button.is_visible():
                print("no Next button; stopping")
                break
            next_button.click()
            page.wait_for_timeout(2500)
    posts = [json.loads(line) for line in recorder.log_path.open()] if recorder.log_path.exists() else []
    writes = [(e["method"], e["url"][:100]) for e in posts if e["method"] != "GET"]
    print(f"api calls: {recorder.count}; non-GET calls: {writes or 'none'}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
