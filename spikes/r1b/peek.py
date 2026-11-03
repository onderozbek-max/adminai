"""Screenshot every open tab of the spike Chrome (CDP on localhost:9223). Read-only."""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
label = sys.argv[1] if len(sys.argv) > 1 else "peek"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
    for ctx in browser.contexts:
        for i, page in enumerate(ctx.pages):
            path = OUT / f"{label}-{i}.png"
            page.screenshot(path=str(path))
            print(f"tab {i}: {page.url} title={page.title()!r} -> {path.name}")
