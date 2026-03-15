"""Lightweight NER helpers for PANOPTO post tagging."""

from __future__ import annotations

import re
from typing import Any

_LOCATION_GAZETTEER: dict[str, tuple[str, float, float]] = {
    "new york": ("New York", 40.7128, -74.0060),
    "united states of america": ("United States", 39.8283, -98.5795),
    "united states": ("United States", 39.8283, -98.5795),
    "usa": ("United States", 39.8283, -98.5795),
    "u.s.": ("United States", 39.8283, -98.5795),
    "canada": ("Canada", 56.1304, -106.3468),
    "ottawa": ("Ottawa", 45.4215, -75.6972),
    "washington dc": ("Washington DC", 38.9072, -77.0369),
    "washington, dc": ("Washington DC", 38.9072, -77.0369),
    "washington d.c.": ("Washington DC", 38.9072, -77.0369),
    "district of columbia": ("Washington DC", 38.9072, -77.0369),
    "washington": ("Washington", 47.7511, -120.7401),
    "los angeles": ("Los Angeles", 34.0522, -118.2437),
    "san francisco": ("San Francisco", 37.7749, -122.4194),
    "boston": ("Boston", 42.3601, -71.0589),
    "chicago": ("Chicago", 41.8781, -87.6298),
    "texas": ("Texas", 31.0, -100.0),
    "california": ("California", 36.7783, -119.4179),
    "florida": ("Florida", 27.6648, -81.5158),
    "ukraine": ("Ukraine", 48.3794, 31.1656),
    "israel": ("Israel", 31.0461, 34.8516),
    "palestine": ("Palestine", 31.9522, 35.2332),
    "gaza": ("Gaza", 31.3547, 34.3088),
    "london": ("London", 51.5072, -0.1276),
    "paris": ("Paris", 48.8566, 2.3522),
    "berlin": ("Berlin", 52.52, 13.405),
    "tokyo": ("Tokyo", 35.6762, 139.6503),
    "beijing": ("Beijing", 39.9042, 116.4074),
    "moscow": ("Moscow", 55.7558, 37.6173),
}

_ORG_SUFFIXES = (
    "inc",
    "corp",
    "llc",
    "ltd",
    "committee",
    "agency",
    "department",
    "university",
    "institute",
    "foundation",
)

_PERSON_TITLE_PREFIX = (
    "mr",
    "mrs",
    "ms",
    "dr",
    "sen",
    "rep",
    "president",
)

_WORD_BOUNDARY_CACHE: dict[str, re.Pattern[str]] = {}
_WASHINGTON_DC_VARIANTS = (
    "washington dc",
    "washington, dc",
    "washington d.c.",
    "district of columbia",
)


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def _word_pattern(value: str) -> re.Pattern[str]:
    cached = _WORD_BOUNDARY_CACHE.get(value)
    if cached:
        return cached
    pattern = re.compile(rf"(?<!\w){re.escape(value)}(?!\w)", re.IGNORECASE)
    _WORD_BOUNDARY_CACHE[value] = pattern
    return pattern


def extract_entities(text: str) -> list[dict[str, Any]]:
    content = str(text or "").strip()
    if not content:
        return []

    entities: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    lowered = content.lower()
    for location, (display, lat, lon) in sorted(_LOCATION_GAZETTEER.items(), key=lambda item: -len(item[0])):
        if location == "washington" and any(_word_pattern(variant).search(lowered) for variant in _WASHINGTON_DC_VARIANTS):
            # Avoid ambiguous Washington state tagging when DC context is explicit.
            continue
        pattern = _word_pattern(location)
        if not pattern.search(lowered):
            continue
        key = ("location", display.lower())
        if key in seen:
            continue
        seen.add(key)
        entities.append(
            {
                "type": "location",
                "text": display,
                "tag": f"loc:{_slugify(display)}",
                "lat": lat,
                "lon": lon,
            }
        )

    for match in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b", content):
        candidate = match.group(1).strip()
        normalized = candidate.lower()
        if ("location", normalized) in seen:
            continue

        first_token = normalized.split()[0]
        if first_token in _PERSON_TITLE_PREFIX:
            person_text = candidate.split(maxsplit=1)[-1] if " " in candidate else candidate
            key = ("person", person_text.lower())
            if key in seen:
                continue
            seen.add(key)
            entities.append(
                {
                    "type": "person",
                    "text": person_text,
                    "tag": f"person:{_slugify(person_text)}",
                }
            )
            continue

        # Heuristic org detection for title-cased multi-word terms.
        tail = normalized.split()[-1]
        if tail in _ORG_SUFFIXES:
            key = ("org", normalized)
            if key in seen:
                continue
            seen.add(key)
            entities.append(
                {
                    "type": "org",
                    "text": candidate,
                    "tag": f"org:{_slugify(candidate)}",
                }
            )
            continue

        if len(candidate.split()) == 2:
            key = ("person", normalized)
            if key in seen:
                continue
            seen.add(key)
            entities.append(
                {
                    "type": "person",
                    "text": candidate,
                    "tag": f"person:{_slugify(candidate)}",
                }
            )

    entities.sort(key=lambda item: (item.get("type", ""), item.get("text", "")))
    return entities
