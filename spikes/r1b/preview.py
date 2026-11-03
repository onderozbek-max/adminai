"""Spike R1b: press PREVIEW on a project dashboard and record the previewer (read-only).

Usage: python preview.py <label> <project_id>
"""
import re
import sys

from playwright.sync_api import sync_playwright

from record import OUT, Recorder, visible_controls


PREVIEW_LABEL = re.compile(r"^\s*preview\s*$", re.I)


def open_previewer(context, project_id: str):
    """Open a project dashboard, press PREVIEW, and return the previewer page."""
    page = context.new_page()
    page.goto(f"https://app.redjade.net/projects/{project_id}/dashboard/")
    button = page.get_by_role("button", name=PREVIEW_LABEL).or_(page.get_by_text(PREVIEW_LABEL)).first
    button.wait_for(timeout=30000)
    pages_before = set(context.pages)
    button.click()
    page.wait_for_timeout(8000)
    new_pages = [pg for pg in context.pages if pg not in pages_before]
    if new_pages:
        page.close()
        return new_pages[0]
    return page


def main(label: str, project_id: str) -> None:
    recorder = Recorder(label)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
        context = browser.contexts[0]
        recorder.attach(context)
        target = open_previewer(context, project_id)
        target.wait_for_timeout(4000)
        target.screenshot(path=str(OUT / f"{label}.png"))
        print(f"url: {target.url}\ntitle: {target.title()!r}")
        print(f"api calls: {recorder.count}")
        print("visible controls:", visible_controls(target)[:60])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
