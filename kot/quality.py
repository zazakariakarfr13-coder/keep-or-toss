"""Quality gates: reading level and the duplicate-page trap-guard."""
from __future__ import annotations

import re
from itertools import combinations

from kot.schema import Food, Guide, LeftOut

_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
_VOWELS = re.compile(r"[aeiouy]+")


def count_syllables(word: str) -> int:
    w = word.lower()
    n = len(_VOWELS.findall(w))
    if w.endswith("e") and not w.endswith("le") and n > 1:
        n -= 1
    return max(n, 1)


def _words(text: str) -> list[str]:
    return _WORD.findall(text)


def reading_grade(text: str) -> float:
    words = _words(text)
    if not words:
        return 0.0
    sentences = max(len([s for s in re.split(r"[.!?]+", text) if _words(s)]), 1)
    syllables = sum(count_syllables(w) for w in words)
    return 0.39 * (len(words) / sentences) + 11.8 * (syllables / len(words)) - 15.59


def kind_of(item) -> str:
    if isinstance(item, Food):
        return "food"
    if isinstance(item, LeftOut):
        return "leftout"
    if isinstance(item, Guide):
        return "guide"
    raise TypeError(f"unknown item type {type(item).__name__}")


def prose_text(item) -> str:
    """Only the page's own prose: no names, titles or sources."""
    k = kind_of(item)
    if k == "food":
        parts = [item.why, *item.spoiled_signs, *item.how_to_store, item.common_mistake, item.freezing]
    elif k == "leftout":
        parts = [item.verdict_line, item.risk, *item.next_time]
    else:
        parts = [item.answer]
        for s in item.sections:
            parts += [*s.paragraphs, *s.bullets]
    return " ".join(p for p in parts if p)


def prose_words(item) -> int:
    return len(_words(prose_text(item)))


def _shingles(text: str, k: int) -> set[tuple[str, ...]]:
    w = [x.lower() for x in _words(text)]
    return {tuple(w[i:i + k]) for i in range(len(w) - k + 1)}


def similarity(a: str, b: str, k: int = 5) -> float:
    sa, sb = _shingles(a, k), _shingles(b, k)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def find_duplicates(items, threshold: float) -> list[tuple[str, str, float]]:
    texts = [(i.slug, prose_text(i)) for i in items]
    out = []
    for (sa, ta), (sb, tb) in combinations(texts, 2):
        s = similarity(ta, tb)
        if s > threshold:
            out.append((sa, sb, round(s, 3)))
    return out
