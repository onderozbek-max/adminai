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
    lines = [line.strip() for line in page.locator("body").inner_text().splitlines()]
    return [bad for bad in BAD_TEXT if bad in lines] + [line for line in lines if "[object" in line]


def phone_text(page) -> str:
    return page.locator(".phone-screen").inner_text()


def test_it_opens_on_the_first_screen_with_a_must_fix_and_that_issue_selected(browser, base_url):
    page, errors = open_page(browser, base_url)
    assert "Q7" in page.locator(".phone-bar").inner_text()
    assert "Q7" in page.locator(".rail-item.on").inner_text()
    first = page.locator(".card").first
    assert "Must fix" in first.inner_text() and "Image didn't load: Relaxed fit" in first.inner_text()
    assert page.locator(".pin.on").get_attribute("aria-label").startswith("Issue 1")
    assert not stray_text(page) and errors == []


def test_the_header_scores_only_what_was_checked_and_says_so(browser, base_url):
    page, _ = open_page(browser, base_url)
    header = page.locator("#topbar").inner_text()
    assert "of 46 checked" in header and "54 points and 3 launch checks wait on the AI step" in header
    assert "Needs work. Fix 1 thing first." in header
    assert "83" not in header and "84" not in header and "63%" not in header   # no 0-100 figure, no bare percentage


@pytest.mark.parametrize("sample", [0, 1])
def test_every_screen_renders_real_text(browser, base_url, sample):
    page, errors = open_page(browser, base_url)
    page.locator("select").select_option(index=sample)
    for i in range(page.locator(".rail-item").count()):
        page.locator(".rail-item").nth(i).click()
        assert "[object" not in phone_text(page) and "undefined" not in phone_text(page)
        assert not stray_text(page)
    assert errors == []


@pytest.mark.parametrize("width", [320, 390, 768, 1280])
def test_page_reflows_without_sideways_scroll(browser, base_url, width):
    page, _ = open_page(browser, base_url, width)
    page.locator(".rail-item").nth(3).click()
    assert page.evaluate("document.documentElement.scrollWidth") <= width


def test_clicking_a_pin_selects_its_card_and_moves_focus_there(browser, base_url):
    page, _ = open_page(browser, base_url)
    page.locator('.pin[aria-label^="Issue 2"]').click()       # the "Click" pin
    assert page.locator(".card.selected").inner_text().startswith("2")
    assert page.evaluate("document.activeElement.className") == "card-head"
    assert "desktop word" in page.evaluate("document.activeElement.textContent")


def test_focus_stays_on_the_control_the_user_used(browser, base_url):
    page, _ = open_page(browser, base_url)
    page.get_by_role("button", name="Large text").focus()
    page.keyboard.press("Enter")
    assert page.evaluate("document.activeElement.dataset.fk") == "large"
    page.locator(".rail-item").nth(2).focus()
    page.keyboard.press("Enter")
    assert page.evaluate("document.activeElement.dataset.fk") == "rail-2"


def test_with_fixes_shows_the_survey_as_it_would_read_and_your_pick_wins(browser, base_url):
    page, _ = open_page(browser, base_url)
    assert "Click" in phone_text(page)
    page.get_by_role("button", name="With fixes").click()
    assert "Tap the one you like best." in phone_text(page) and "Click the one" not in phone_text(page)
    assert "Fixed in preview" in page.locator(".card").nth(1).inner_text()
    page.locator(".card").nth(1).get_by_label("Your original").check()      # the researcher overrules the coach
    assert "Tap the one" not in phone_text(page) and "Click" in phone_text(page)   # a pin sits between the words


def test_with_fixes_applies_to_options_and_the_intro_and_adds_suggested_questions(browser, base_url):
    page, _ = open_page(browser, base_url)
    page.get_by_role("button", name="With fixes").click()
    page.locator(".rail-item").first.click()                                  # Intro
    assert "takes about 4 minutes. [Say what members get for finishing.]" in phone_text(page)
    page.locator(".rail-item", has_text="Q2").click()
    assert "1 to 4 years" in phone_text(page) and "1 to 5 years" not in phone_text(page)
    page.locator(".rail-item", has_text="Q10").click()
    page.get_by_role("button", name="Next screen").click()                    # Q11: the scale end gets its label
    assert "Extremely likely" in phone_text(page)


def test_copy_puts_only_the_suggested_text_on_the_clipboard(browser, base_url):
    page, _ = open_page(browser, base_url)
    page.locator(".card").nth(1).get_by_role("button", name="Copy suggested text").click()
    page.wait_for_function("document.querySelector('.card.selected, .card [role=status]') !== null")
    assert page.evaluate("navigator.clipboard.readText()") == "Tap the one you like best."
    assert "does not change your survey" in page.locator(".card").nth(1).inner_text()


def test_findings_without_a_real_fix_have_no_copy_button(browser, base_url):
    page, _ = open_page(browser, base_url)
    assert page.locator(".card").first.get_by_role("button", name="Copy suggested text").count() == 0


def test_unchecked_areas_are_not_drawn_as_earned(browser, base_url):
    page, _ = open_page(browser, base_url)
    page.get_by_text("Score by area").click()
    assert page.locator(".areas i.wait").count() > 0
    assert "waiting" in page.locator(".areas").inner_text() or "Not checked yet" in page.locator(".areas").inner_text()


def test_clean_sample_has_no_cards_and_is_not_called_ready(browser, base_url):
    page, _ = open_page(browser, base_url)
    page.locator("select").select_option(index=1)
    assert page.locator(".card").count() == 0
    assert "Nothing to fix yet" in page.locator("#topbar").inner_text() and "Ready to launch" not in page.locator("body").inner_text()
    assert "of 46 checked" in page.locator("#topbar").inner_text()                  # never an unqualified full ring
    assert "Nothing flagged yet" in page.locator(".rail").inner_text() and "No issues found" not in page.locator(".rail").inner_text()
    assert not stray_text(page)


def test_on_a_phone_the_phone_is_the_hero_and_opens_on_the_problem(browser, base_url):
    page, _ = open_page(browser, base_url, 390)
    phone = page.locator(".phone").bounding_box()
    assert phone["y"] < 380 and phone["y"] < page.locator(".coach").bounding_box()["y"]
    assert page.get_by_role("group", name="Device").is_hidden()
    assert "Image didn't load: Relaxed fit" in page.locator(".lead").inner_text()   # the top issue, above the phone
    pin, screen = page.locator('.pin[aria-label^="Issue 1"]').bounding_box(), page.locator(".phone-screen").bounding_box()
    assert screen["y"] <= pin["y"] and pin["y"] + pin["height"] <= screen["y"] + screen["height"]   # pin 1 is in view


def test_suggestions_mark_only_the_words_that_change(browser, base_url):
    page, _ = open_page(browser, base_url)
    card = page.locator(".card").nth(1)
    assert card.locator("del").inner_text() == "Click" and card.locator("ins").inner_text() == "Tap"


def test_the_ring_never_draws_unchecked_points_as_earned(browser, base_url):
    page, _ = open_page(browser, base_url)
    ring = page.locator(".ring")
    earned, checked = (float(ring.evaluate(f"el => getComputedStyle(el).getPropertyValue('--{v}')").strip().replace("deg", "")) for v in "ek")
    assert earned < checked < 360                       # earned < checked < everything: a grey 'waiting' arc always remains
