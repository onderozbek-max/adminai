"""Spike R1c: RedJade questionnaire definition (captured passively) and coverage-first answer policy."""
import json
import re
from pathlib import Path

TAG = re.compile(r"<[^>]+>")
EXCLUSIVE = re.compile(r"didn.?t|nothing|none of|^none|prefer not|don.?t know|not sure|something else|other", re.I)


def clean(html: str) -> str:
    text = TAG.sub(" ", html or "").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", text).strip()


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


class Definition:
    """Questionnaire pages, answers, and triggers from RedJade's in-progress payload."""

    def __init__(self, payload: dict):
        q = payload["questionnaire"]
        self.title = q.get("questionnaire_type")
        self.pages = q["data"]["pages"]
        self.answers = {}      # answer id -> (page index, question cid, text)
        self.trigger_refs = {}  # answer id -> number of later pages it can unlock ("any" triggers)
        for page in self.pages:
            for question in page["questions"]:
                for a in question.get("answers", []):
                    self.answers[a["id"]] = (page["index"], question.get("cid"), clean(a["text"].get("en_US", "")))
        for page in self.pages:
            for t in page.get("triggers", []):
                if t.get("condition") == "any":
                    for aid in t.get("answers", []):
                        self.trigger_refs[aid] = self.trigger_refs.get(aid, 0) + 1

    @classmethod
    def find_in(cls, bodies_dir: Path) -> "Definition | None":
        for path in sorted(bodies_dir.glob("*.json"), reverse=True):
            data = json.loads(path.read_text())
            data = data.get("response", data)
            if isinstance(data, dict) and isinstance(data.get("questionnaire"), dict) \
                    and "pages" in data["questionnaire"].get("data", {}):
                return cls(data)
        return None

    def page_for(self, visible_text: str) -> dict | None:
        """Match the visible page to a definition page by its question text."""
        seen = norm(visible_text)
        best, best_len = None, 0
        for page in self.pages:
            for question in page["questions"]:
                prompt = norm(clean(question.get("text", {}).get("en_US", "")))[:60]
                if prompt and prompt in seen and len(prompt) > best_len:
                    best, best_len = page, len(prompt)
        return best

    def choose(self, page: dict) -> list[str]:
        """Coverage-first: answer texts that unlock the most later pages; never opt-outs."""
        chosen = []
        for question in page["questions"]:
            answers = question.get("answers", [])
            if not answers:
                continue
            usable = [a for a in answers if not EXCLUSIVE.search(clean(a["text"].get("en_US", "")))] or answers
            unlocking = [a for a in usable if self.trigger_refs.get(a["id"])]
            if question["question_type"] == "checkbox":
                picks = unlocking or usable[:1]
            else:
                picks = [max(unlocking, key=lambda a: self.trigger_refs[a["id"]])] if unlocking else [usable[0]]
            chosen += [clean(a["text"].get("en_US", "")) for a in picks]
        return chosen

    def is_last(self, page: dict, selected_ids: set[str]) -> bool:
        """True when no later page can be shown, given the answers selected so far."""
        for later in self.pages[page["index"] + 1:]:
            triggers = later.get("triggers", [])
            if not triggers or any(self._satisfied(t, selected_ids) for t in triggers):
                return False
        return True

    @staticmethod
    def _satisfied(trigger: dict, selected: set[str]) -> bool:
        wanted = set(trigger.get("answers", []))
        if trigger.get("condition") == "equal":
            return bool(wanted) and wanted <= selected
        return bool(wanted & selected)

    def ids_for(self, texts: list[str]) -> set[str]:
        wanted = {norm(t) for t in texts}
        return {aid for aid, (_, _, text) in self.answers.items() if norm(text) in wanted}

    def summary(self) -> str:
        lines = []
        for page in self.pages:
            for q in page["questions"]:
                gate = " (conditional)" if page.get("triggers") else ""
                lines.append(f"p{page['index']} {q['question_type']}{gate}: {clean(q.get('text', {}).get('en_US', ''))[:70]}")
        return "\n".join(lines)
