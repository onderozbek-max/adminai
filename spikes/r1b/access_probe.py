"""Spike R1b: does the previewer API serve an event whose project isn't shared with this user?

Runs fetch() inside the RedJade tab so the session token never leaves the browser.
Only HTTP status codes and sizes are returned. Read-only (GET).
"""
from playwright.sync_api import sync_playwright

PROBE_JS = """async (eventIds) => {
  const keys = Object.keys(localStorage);
  const tokenKey = keys.find(k => /auth|token/i.test(k));
  let token = tokenKey ? localStorage.getItem(tokenKey) : null;
  try { const parsed = JSON.parse(token); token = parsed.access_token || parsed.token || parsed; } catch (e) {}
  const results = {storageKeyNames: keys, usedKey: tokenKey};
  for (const id of eventIds) {
    const r = await fetch(`/api/v1/survey_previewer/servings?event_id=${id}&participant_code=&verification_code=`,
        {headers: {Authorization: `Bearer ${token}`, Accept: 'application/json'}, credentials: 'include'});
    const text = await r.text();
    results[id] = {status: r.status, bytes: text.length, error: r.ok ? null : text.slice(0, 160)};
  }
  return results;
}"""

EVENTS = {"500801": "Cashews (shared with Onder)", "502476": "Cakeballs (not shared)"}

with sync_playwright() as p:
    context = p.chromium.connect_over_cdp("http://127.0.0.1:9223").contexts[0]
    page = context.new_page()
    page.goto("https://app.redjade.net/home/")
    page.wait_for_timeout(5000)
    result = page.evaluate(PROBE_JS, list(EVENTS))
    page.close()

print("localStorage key names:", result.pop("storageKeyNames"), "| used:", result.pop("usedKey"))
for event_id, label in EVENTS.items():
    print(f"{label} event {event_id}: {result[event_id]}")
