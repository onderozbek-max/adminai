"""Spike R1b: open a RedJade page in a new tab of the spike Chrome and record API traffic.

Read-only by intent: only navigates; never clicks. Secrets are redacted before writing.
Usage: python record.py <label> <url> [seconds]
"""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
SECRET_HEADERS = re.compile(r"authorization|cookie|token|csrf|session", re.I)
SECRET_KEYS = re.compile(r"token|password|secret|auth|cookie|^enc$|jwt|session", re.I)


def redact(value):
    if isinstance(value, dict):
        return {k: ("<redacted>" if SECRET_KEYS.search(k) else redact(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


class Recorder:
    """Logs redacted /api/ traffic for every page in a browser context."""

    def __init__(self, label: str):
        self.log_path = OUT / f"{label}-network.jsonl"
        self.bodies = OUT / f"{label}-bodies"
        self.bodies.mkdir(exist_ok=True)
        self.count = 0

    def attach(self, context) -> None:
        context.on("response", self.on_response)

    def on_response(self, response):
        req = response.request
        if "/api/" not in req.url:
            return
        self.count += 1
        count = self.count
        bodies = self.bodies
        entry = {
            "n": count,
            "method": req.method,
            "url": req.url,
            "status": response.status,
            "req_headers": {k: v for k, v in req.headers.items() if not SECRET_HEADERS.search(k)},
            "post_data": redact(_json_or_none(req.post_data)) if req.post_data else None,
        }
        try:
            data = response.json()
            body_file = bodies / f"{count:03d}.json"
            body_file.write_text(json.dumps(redact(data), indent=1))
            entry["body_file"] = body_file.name
            entry["body_bytes"] = body_file.stat().st_size
        except Exception:
            entry["body_file"] = None
        with self.log_path.open("a") as fh:
            fh.write(json.dumps(entry) + "\n")


def visible_controls(page) -> list[str]:
    controls = page.locator("a, button").all()
    return sorted({(c.inner_text() or "").strip()[:40] for c in controls if c.is_visible()} - {""})


def main(label: str, url: str, seconds: int) -> None:
    recorder = Recorder(label)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
        context = browser.contexts[0]
        recorder.attach(context)
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(seconds * 1000)
        page.screenshot(path=str(OUT / f"{label}.png"))
        print(f"url now: {page.url}\ntitle: {page.title()!r}\napi calls: {recorder.count}")
        print("visible controls:", visible_controls(page)[:80])
        page.close()


def _json_or_none(text):
    try:
        return json.loads(text)
    except Exception:
        return {"raw_len": len(text)}


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8)
