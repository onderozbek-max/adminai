"""Browser checks for the static demo in site/. Skipped when Playwright or its Chromium is unavailable."""
import functools
import http.server
import threading
from pathlib import Path

import pytest

sync_api = pytest.importorskip("playwright.sync_api")
SITE = Path(__file__).parent.parent / "site"
BAD_TEXT = ("false", "undefined", "null", "NaN", "[object Object]")


@pytest.fixture(scope="module")
def base_url():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))
    handler.log_message = lambda *args: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}/"
    server.shutdown()


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as p:
        try:
            chromium = p.chromium.launch()
        except Exception as error:   # browser not installed on this machine
            pytest.skip(f"Chromium unavailable: {error}")
        yield chromium
        chromium.close()


def open_page(browser, base_url, width=1280):
    context = browser.new_context(viewport={"width": width, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.goto(base_url)
    return page, errors


def stray_text(page) -> list[str]:
    lines = [line.strip() for line in page.locator("main").inner_text().splitlines()]
    return [bad for bad in BAD_TEXT if bad in lines] + [line for line in lines if "[object" in line]


@pytest.mark.parametrize("sample", [0, 1])
def test_every_phone_screen_renders_real_text(browser, base_url, sample):
    page, errors = open_page(browser, base_url)
    page.locator(".picker label").nth(sample).click()
    total = int(page.locator(".phone-bar span").first.inner_text().split(" of ")[1])
    for _ in range(total):
        body = page.locator(".phone-screen").inner_text()
        assert "[object" not in body and "undefined" not in body, body[:100]
        assert not stray_text(page)
        if page.get_by_role("button", name="Next screen").is_enabled():
            page.get_by_role("button", name="Next screen").click()
    assert errors == []


@pytest.mark.parametrize("width", [320, 390, 768, 1280])
def test_page_reflows_without_sideways_scroll(browser, base_url, width):
    page, _ = open_page(browser, base_url, width)
    page.locator(".finding-list .row").nth(3).click()
    assert page.evaluate("document.documentElement.scrollWidth") <= width


def test_selecting_a_finding_opens_its_detail_and_jumps_the_phone(browser, base_url):
    page, errors = open_page(browser, base_url)
    first = page.locator(".finding-list .row").first
    first.click()
    assert first.get_attribute("aria-expanded") == "true"
    assert page.evaluate("document.activeElement.dataset.idx") == "0"          # focus survives the re-render
    assert "Screen 8 of 13" in page.locator(".phone-bar").inner_text()          # the must-fix is on screen 8
    assert "Coach flagged this question" in page.locator(".q.selected").inner_text()
    assert not stray_text(page) and errors == []


def test_copy_suggestion_copies_the_fix_and_says_nothing_was_changed(browser, base_url):
    page, _ = open_page(browser, base_url)
    page.locator(".finding-list .row").first.click()
    page.get_by_role("button", name="Copy suggestion").click()
    page.wait_for_function("document.querySelector('#finding-detail p[role=status]').textContent.length > 0")
    assert "does not change your survey" in page.locator("#finding-detail p[role=status]").inner_text()
    assert "Fix or replace the image" in page.evaluate("navigator.clipboard.readText()")


def test_clean_sample_shows_no_findings_and_is_still_not_ready(browser, base_url):
    page, _ = open_page(browser, base_url)
    page.locator(".picker label").nth(1).click()
    assert page.locator(".finding-list .row").count() == 0
    assert "Almost ready" in page.locator("#summary").inner_text()
    assert not stray_text(page)
