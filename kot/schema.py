"""Data types for every page, and validation that runs before any build."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal

from kot import config

_UNIT_HOURS = {"hours": 1, "days": 24, "weeks": 168, "months": 720, "years": 8760}
_SLUG = re.compile(r"^[a-z0-9-]+$")


@dataclass
class Span:
    min: float
    max: float
    unit: Literal["hours", "days", "weeks", "months", "years"]
    note: str = ""

    def __post_init__(self):
        if self.unit not in _UNIT_HOURS:
            raise ValueError(f"unknown unit {self.unit!r}")
        if self.min > self.max:
            raise ValueError(f"span min {self.min} is above max {self.max}")

    def max_hours(self) -> float:
        return self.max * _UNIT_HOURS[self.unit]


@dataclass
class Source:
    publisher: str
    title: str
    url: str


@dataclass
class Food:
    slug: str
    name: str
    category: str
    question: str
    storage: dict[str, Span | None]
    why: str
    spoiled_signs: list[str]
    how_to_store: list[str]
    common_mistake: str
    freezing: str
    sources: list[Source]
    related: list[str]
    description: str


@dataclass
class QuickFood:
    """A food with official storage times but no page of its own (search + checker only)."""
    slug: str
    name: str
    category: str
    storage: dict[str, Span | None]
    source: str


@dataclass
class LeftOut:
    slug: str
    food: str
    question: str
    verdict: Literal["toss", "keep", "depends"]
    verdict_line: str
    risk: str
    next_time: list[str]
    sources: list[Source]
    related: list[str]
    description: str


@dataclass
class Section:
    heading: str
    paragraphs: list[str]
    bullets: list[str] = field(default_factory=list)


@dataclass
class Guide:
    slug: str
    kind: Literal["country", "emergency", "bridge", "seasonal"]
    title: str
    description: str
    answer: str
    sections: list[Section]
    sources: list[Source]
    related: list[str]


def validate_all(foods: list[Food], leftout: list[LeftOut], guides: list[Guide],
                 quick: list[QuickFood] | None = None) -> None:
    """Raise ValueError naming the slug and problem for the first issue found."""
    seen: set[str] = set()
    quick = quick or []
    for item in [*foods, *leftout, *guides]:
        if not _SLUG.match(item.slug):
            raise ValueError(f"{item.slug!r}: slug must be lowercase letters, digits and dashes")
        if item.slug in seen:
            raise ValueError(f"{item.slug}: duplicate slug")
        seen.add(item.slug)
        if not item.sources:
            raise ValueError(f"{item.slug}: needs at least one source")

    food_slugs = {f.slug for f in foods}
    for f in foods:
        if f.category not in config.CATEGORIES:
            raise ValueError(f"{f.slug}: unknown category {f.category!r}")
        if not f.storage:
            raise ValueError(f"{f.slug}: needs at least one storage place")
        for place in f.storage:
            if place not in config.PLACES:
                raise ValueError(f"{f.slug}: unknown place {place!r}")
    for lo in leftout:
        if lo.food not in food_slugs:
            raise ValueError(f"{lo.slug}: unknown food {lo.food!r}")
        if lo.verdict not in ("toss", "keep", "depends"):
            raise ValueError(f"{lo.slug}: unknown verdict {lo.verdict!r}")
    for g in guides:
        if g.kind not in ("country", "emergency", "bridge", "seasonal"):
            raise ValueError(f"{g.slug}: unknown kind {g.kind!r}")
    for q in quick:
        if not _SLUG.match(q.slug):
            raise ValueError(f"{q.slug!r}: slug must be lowercase letters, digits and dashes")
        if q.slug in seen:
            raise ValueError(f"{q.slug}: duplicate slug (quick food)")
        seen.add(q.slug)
        if q.category not in config.CATEGORIES:
            raise ValueError(f"{q.slug}: unknown category {q.category!r}")
        if not q.storage:
            raise ValueError(f"{q.slug}: needs at least one storage place")
        for place in q.storage:
            if place not in config.PLACES:
                raise ValueError(f"{q.slug}: unknown place {place!r}")
    for item in [*foods, *leftout, *guides]:
        for r in item.related:
            if r not in seen:
                raise ValueError(f"{item.slug}: related slug {r!r} does not exist")
