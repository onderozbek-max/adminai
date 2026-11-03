"""Spike R1b: point RedJade's own previewer at another event via its stored event id.

No token handling: the previewer app makes its own authenticated calls. Read-only (preview mode).
Usage: python event_probe.py <label> <event_id>
"""
import json
import sys

from playwright.sync_api import sync_playwright

from record import OUT, Recorder


def main(label: str, event_id: str) -> None:
    recorder = Recorder(label)
    with sync_playwright() as p:
        context = p.chromium.connect_over_cdp("http://127.0.0.1:9223").contexts[0]
        recorder.attach(context)
        page = context.new_page()
        page.goto("https://app.redjade.net/home/")
        page.wait_for_timeout(3000)
        before = page.evaluate("() => localStorage.getItem('ls.previewer_event_id')")
        page.evaluate("(id) => localStorage.setItem('ls.previewer_event_id', JSON.stringify(Number(id)))", event_id)
        page.goto("https://app.redjade.net/previewer/questionnaire")
        page.wait_for_timeout(8000)
        page.screenshot(path=str(OUT / f"{label}.png"))
        print(f"stored event id before: {before}; now: {event_id}; url: {page.url}")
        page.close()
    for line in recorder.log_path.open():
        e = json.loads(line)
        print(e["method"], e["status"], e["url"][:120], e.get("body_bytes"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
