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
