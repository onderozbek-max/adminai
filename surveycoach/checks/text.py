"""Small, dependency-free text measurements shared by the content checks."""
from __future__ import annotations

import re

WORD = re.compile(r"[A-Za-z][A-Za-z'\u2019]*")
SENTENCE_END = re.compile(r"(?<=[.?!])\s+")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B55\u23E9-\u23FA]")
# Capitalized mid-sentence function words are the signature of Title Case.
FUNCTION_WORDS = {"Do", "Does", "Did", "You", "Your", "Of", "The", "And", "To", "In", "Is", "Are", "Or", "For",
                  "At", "On", "With", "By", "From", "Than", "That", "This", "It", "Be", "Have", "Has", "Was", "Were"}


def count_syllables(word: str) -> int:
    word = word.lower().strip("'\u2019")
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    if word.endswith("e") and not word.endswith(("le", "ee")) and count > 1:
        count -= 1
    return max(1, count)


def reading_grade(text: str) -> float:
    """Flesch-Kincaid grade level. Higher means harder to read."""
    words = WORD.findall(text)
    if not words:
        return 0.0
    sentences = max(1, len([s for s in SENTENCE_END.split(text.strip()) if s]))
    syllables = sum(count_syllables(w) for w in words)
    return 0.39 * len(words) / sentences + 11.8 * syllables / len(words) - 15.59


def emoji_count(text: str) -> int:
    return len(EMOJI.findall(text or ""))


def has_emoji(text: str) -> bool:
    return emoji_count(text) > 0


def title_case_signature(text: str) -> bool:
    """True when a function word like Do, You, or At is capitalized mid-sentence."""
    for sentence in SENTENCE_END.split(text):
        tokens = [t.strip("\"'()?!.,:;") for t in sentence.split()]
        if any(t in FUNCTION_WORDS for t in tokens[1:]):
            return True
    return False


def plural(count: int, noun: str) -> str:
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def swap_word(text: str, old: str, new: str) -> str:
    """Replace a whole word, keeping a leading capital. An empty `new` removes the word and its space."""
    def pick(match: re.Match) -> str:
        found = match.group(0)
        return new[:1].upper() + new[1:] if found[:1].isupper() and new else new
    swapped = re.sub(rf"\b{re.escape(old)}\b", pick, text, flags=re.I)
    return re.sub(r"\s{2,}", " ", swapped).replace(" ,", ",").replace(" .", ".").strip()


PROTECTED_NAMES = ("Member's Mark", "Member\u2019s Mark", "Sam's Club", "Sam\u2019s Club", "RedJade", "MMC")


def sentence_case(text: str) -> str:
    """Lowercase everything except the first word of each sentence, acronyms, and brand names."""
    held = {f"\x00{i}\x00": name for i, name in enumerate(PROTECTED_NAMES)}
    for token, name in held.items():
        text = text.replace(name, token)

    def fix_sentence(sentence: str) -> str:
        words = sentence.split(" ")
        fixed = [w if (i == 0 or w.isupper() or "\x00" in w) else w.lower() for i, w in enumerate(words)]
        fixed[0] = fixed[0][:1].upper() + fixed[0][1:]
        return " ".join(fixed)

    result = " ".join(fix_sentence(s) for s in SENTENCE_END.split(text))
    for token, name in held.items():
        result = result.replace(token, name)
    return result


def limit_emoji(text: str, keep: int = 0) -> str:
    """Remove emoji beyond the first `keep`, and the space left behind."""
    seen = 0

    def drop(match: re.Match) -> str:
        nonlocal seen
        seen += 1
        return match.group(0) if seen <= keep else ""
    return re.sub(r"\s{2,}", " ", EMOJI.sub(drop, text)).strip()
