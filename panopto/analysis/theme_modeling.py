"""Theme tagging using BERTopic for collected social posts."""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from panopto.storage.posts import init_db

_SLUG_CLEAN = re.compile(r"[^a-z0-9]+")
_VIEW_PROFILE = re.compile(r"\bview profile\b", re.IGNORECASE)
_PROFILE_TOKEN = re.compile(r"\bprofile\b", re.IGNORECASE)
_AT_HANDLE = re.compile(r"(?<!\w)@\w+", re.IGNORECASE)
_URL = re.compile(r"https?://\S+", re.IGNORECASE)
_SPACE = re.compile(r"\s+")
_ACTION_NOISE = re.compile(
    r"\b(?:screenshot|share|view profile|watch on twitter(?:/x)?|download(?: video| gif| image)?)\b",
    re.IGNORECASE,
)
_METRIC_NOISE = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*[kKmM]?\s*(?:likes?|retweets?|reposts?|replies?|comments?|views?)\b",
    re.IGNORECASE,
)
_NUMERIC_COUNTER_TAIL = re.compile(
    r"(?:\b\d+(?:[.,]\d+)?\s*[kKmM]?\b(?:\s+\b\d+(?:[.,]\d+)?\s*[kKmM]?\b){1,7})\s*$",
    re.IGNORECASE,
)
_DATE_TOKEN = re.compile(
    r"\b(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}(?:st|nd|rd|th)?\s+"
    r"(?:jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|"
    r"sep|sept|september|oct|october|nov|november|dec|december)\b)\b",
    re.IGNORECASE,
)
_TIME_RECENCY_TOKEN = re.compile(
    r"\b(?:\d+\s*[smhdwy]|"
    r"\d+\s*(?:sec(?:ond)?s?|min(?:ute)?s?|hr(?:s)?|hour(?:s)?|day(?:s)?|week(?:s)?|month(?:s)?|year(?:s)?)|"
    r"\d{1,2}:\d{2}(?:\s?[ap]m)?|"
    r"today|yesterday|tomorrow|tonight|now|recent(?:ly)?|current(?:ly)?|latest)\b",
    re.IGNORECASE,
)
_DATE_LIKE_WORD = re.compile(
    r"^(?:\d{4}|"
    r"\d{1,2}(?:st|nd|rd|th)?|"
    r"\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?|"
    r"jan|january|feb|february|mar|march|apr|april|may|jun|june|"
    r"jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december"
    r")$",
    re.IGNORECASE,
)
_TEMPORAL_LIKE_WORD = re.compile(
    r"^(?:"
    r"\d{1,4}|"
    r"\d+[smhdwy]|"
    r"\d{1,2}:\d{2}(?:[ap]m)?|"
    r"\d+(?:sec(?:ond)?s?|min(?:ute)?s?|hr(?:s)?|hour(?:s)?|day(?:s)?|week(?:s)?|month(?:s)?|year(?:s)?)|"
    r"today|yesterday|tomorrow|tonight|now|recent(?:ly)?|current(?:ly)?|latest|"
    r"jan|january|feb|february|mar|march|apr|april|may|jun|june|"
    r"jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december"
    r")$",
    re.IGNORECASE,
)


def _slugify(value: str) -> str:
    cleaned = _SLUG_CLEAN.sub("-", value.lower()).strip("-")
    return cleaned or "misc"


def _topic_label(topic_words: list[tuple[str, float]] | None) -> tuple[str, list[str]]:
    if not topic_words:
        return "misc", ["misc"]
    words = [
        word
        for word, _score in topic_words
        if word
        and not _DATE_LIKE_WORD.match(str(word).strip())
        and not _TEMPORAL_LIKE_WORD.match(str(word).strip())
    ][:3]
    if not words:
        return "misc", ["misc"]
    return " / ".join(words), words


def _prepare_document(text: str, username: str) -> str:
    cleaned = (text or "").strip()
    if not cleaned:
        return ""
    if username:
        cleaned = re.sub(
            rf"^\s*[^@\n]{{1,80}}\s+@{re.escape(username)}\s*(?:[·•-]\s*[^ \n]+)?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )
    cleaned = _URL.sub(" ", cleaned)
    cleaned = _VIEW_PROFILE.sub(" ", cleaned)
    cleaned = _PROFILE_TOKEN.sub(" ", cleaned)
    cleaned = _AT_HANDLE.sub(" ", cleaned)
    cleaned = _ACTION_NOISE.sub(" ", cleaned)
    cleaned = _METRIC_NOISE.sub(" ", cleaned)
    cleaned = _DATE_TOKEN.sub(" ", cleaned)
    cleaned = _TIME_RECENCY_TOKEN.sub(" ", cleaned)
    cleaned = _NUMERIC_COUNTER_TAIL.sub(" ", cleaned)
    cleaned = _SPACE.sub(" ", cleaned).strip(" .-")
    return cleaned


def _load_documents(db_path: Path) -> tuple[list[int], list[str]]:
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, username, content
            FROM twitter_posts
            WHERE COALESCE(TRIM(content), '') != ''
            ORDER BY id ASC
            """
        ).fetchall()
    post_ids: list[int] = []
    docs: list[str] = []
    for row in rows:
        cleaned = _prepare_document(str(row[2] or ""), str(row[1] or ""))
        if not cleaned:
            continue
        post_ids.append(int(row[0]))
        docs.append(cleaned)
    return post_ids, docs


def _clear_theme_columns(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE twitter_posts
            SET topic_id = NULL,
                theme_label = NULL,
                theme_keywords = NULL,
                theme_tag = NULL
            """
        )
        conn.commit()


def _tag_with_bertopic(docs: list[str], min_topic_size: int) -> tuple[list[int], dict[int, tuple[str, list[str]]]]:
    from bertopic import BERTopic
    from sklearn.feature_extraction.text import CountVectorizer

    topic_model = BERTopic(
        language="english",
        verbose=False,
        calculate_probabilities=False,
        min_topic_size=max(2, min_topic_size),
        vectorizer_model=CountVectorizer(stop_words="english", ngram_range=(1, 2)),
    )
    topics, _ = topic_model.fit_transform(docs)
    topic_map: dict[int, tuple[str, list[str]]] = {-1: ("misc", ["misc"])}
    for topic_id in sorted({int(topic) for topic in topics if int(topic) >= 0}):
        label, words = _topic_label(topic_model.get_topic(topic_id))
        topic_map[topic_id] = (label, words)
    return [int(topic) for topic in topics], topic_map


def tag_posts_with_bertopic(db_path: str = "osint_data.db", min_topic_size: int = 2) -> dict[str, Any]:
    """Apply BERTopic to all collected posts and persist theme tags."""

    path = Path(db_path)
    if not path.exists():
        return {"status": "skipped", "reason": "db_missing", "tagged": 0, "topics": 0}
    init_db(str(path))

    post_ids, docs = _load_documents(path)
    if not docs:
        _clear_theme_columns(path)
        return {"status": "ok", "reason": "no_docs", "tagged": 0, "topics": 0}

    if len(docs) < 2:
        topic_ids = [0]
        topic_map = {0: ("general", ["general"])}
    else:
        try:
            topic_ids, topic_map = _tag_with_bertopic(docs, min_topic_size=min_topic_size)
        except Exception as exc:  # pragma: no cover - runtime environment dependent
            return {"status": "skipped", "reason": f"bertopic_unavailable: {exc}", "tagged": 0, "topics": 0}

    with sqlite3.connect(path) as conn:
        for post_id, topic_id in zip(post_ids, topic_ids, strict=True):
            label, words = topic_map.get(topic_id, ("misc", ["misc"]))
            conn.execute(
                """
                UPDATE twitter_posts
                SET topic_id = ?,
                    theme_label = ?,
                    theme_keywords = ?,
                    theme_tag = ?
                WHERE id = ?
                """,
                (
                    topic_id,
                    label,
                    json.dumps(words, ensure_ascii=True),
                    f"theme:{_slugify(label)}",
                    post_id,
                ),
            )
        conn.commit()

    return {
        "status": "ok",
        "reason": "tagged",
        "tagged": len(post_ids),
        "topics": len({topic for topic in topic_ids if topic >= 0}),
    }
