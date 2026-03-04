"""Facial-recognition clustering for dashboard media.

Backend priority (accuracy-first):
1) InsightFace ArcFace embeddings (best free option in this project context)
2) OpenCV Haar + lightweight descriptor fallback
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    np = None

try:
    import insightface  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    insightface = None

try:
    import cv2  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    cv2 = None


_PERSON_COLORS = [
    "#ef4444",
    "#22c55e",
    "#0ea5e9",
    "#f59e0b",
    "#e11d48",
    "#8b5cf6",
    "#14b8a6",
    "#f97316",
]


@dataclass(frozen=True)
class _MediaCandidate:
    media_url: str
    analysis_url: str


def _is_http_url(value: str) -> bool:
    lowered = str(value or "").strip().lower()
    return lowered.startswith("https://") or lowered.startswith("http://")


def _is_video_url(value: str) -> bool:
    lowered = str(value or "").strip().lower()
    return (
        ".mp4" in lowered
        or ".m3u8" in lowered
        or "video.twimg.com/" in lowered
        or "v.redd.it/" in lowered
        or "youtube.com/watch?" in lowered
    )


def _is_image_url(value: str) -> bool:
    lowered = str(value or "").strip().lower()
    return any(
        token in lowered
        for token in [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".gif",
            "pbs.twimg.com/media/",
            "preview.redd.it/",
            "ytimg.com/vi/",
        ]
    )


def _normalize_media(post: dict[str, Any]) -> list[dict[str, str]]:
    metadata = post.get("metadata") if isinstance(post.get("metadata"), dict) else {}
    media: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def add_media(kind: str, url: str, thumbnail_url: str = "") -> None:
        value = str(url or "").strip()
        if not _is_http_url(value):
            return
        normalized = kind.lower().strip() or ("video" if _is_video_url(value) else "image")
        key = (normalized, value)
        if key in seen:
            return
        seen.add(key)
        media.append(
            {
                "type": normalized,
                "url": value,
                "thumbnail_url": str(thumbnail_url or "").strip() if _is_http_url(thumbnail_url) else "",
            }
        )

    if isinstance(metadata.get("media"), list):
        for item in metadata["media"]:
            if not isinstance(item, dict):
                continue
            add_media(str(item.get("type") or ""), str(item.get("url") or ""), str(item.get("thumbnail_url") or ""))

    for field in ("video_url", "play_url", "media_url"):
        value = str(metadata.get(field) or "").strip()
        if _is_http_url(value) and _is_video_url(value):
            add_media("video", value, str(metadata.get("thumbnail_url") or ""))

    if isinstance(metadata.get("image_urls"), list):
        for value in metadata["image_urls"]:
            candidate = str(value or "").strip()
            if _is_http_url(candidate) and _is_image_url(candidate):
                add_media("image", candidate)

    if isinstance(metadata.get("media_urls"), list):
        for value in metadata["media_urls"]:
            candidate = str(value or "").strip()
            if not _is_http_url(candidate):
                continue
            if _is_video_url(candidate):
                add_media("video", candidate, str(metadata.get("thumbnail_url") or ""))
            elif _is_image_url(candidate):
                add_media("image", candidate)

    for field in ("image_url", "image", "thumbnail_url", "preview_image_url"):
        candidate = str(metadata.get(field) or "").strip()
        if _is_http_url(candidate) and not _is_video_url(candidate):
            add_media("image", candidate)
    return media


def _media_candidates(post: dict[str, Any]) -> list[_MediaCandidate]:
    rows = _normalize_media(post)
    metadata = post.get("metadata") if isinstance(post.get("metadata"), dict) else {}
    profile_candidates = [
        metadata.get("profile_image_url"),
        metadata.get("profile_image"),
        metadata.get("avatar_url"),
        metadata.get("avatar"),
        metadata.get("author_avatar"),
        metadata.get("user_avatar"),
    ]
    candidates: list[_MediaCandidate] = []
    seen: set[tuple[str, str]] = set()
    for maybe in profile_candidates:
        profile_url = str(maybe or "").strip()
        if not _is_http_url(profile_url):
            continue
        key = (profile_url, profile_url)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(_MediaCandidate(media_url=profile_url, analysis_url=profile_url))
    for item in rows:
        media_url = str(item.get("url") or "").strip()
        thumbnail = str(item.get("thumbnail_url") or "").strip()
        item_type = str(item.get("type") or "image").strip().lower()
        analysis_url = thumbnail if item_type == "video" and _is_http_url(thumbnail) else media_url
        if not _is_http_url(analysis_url):
            continue
        key = (media_url, analysis_url)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(_MediaCandidate(media_url=media_url, analysis_url=analysis_url))
    return candidates


def _cosine_similarity(left: Any, right: Any) -> float:
    denom = float(np.linalg.norm(left) * np.linalg.norm(right))
    if denom <= 0:
        return 0.0
    return float(np.dot(left, right) / denom)


def _normalize_embedding(vector: Any) -> Any:
    arr = np.asarray(vector, dtype=np.float32)
    norm = float(np.linalg.norm(arr))
    if norm > 0:
        arr = arr / norm
    return arr


def _opencv_fallback_descriptor(gray_face: Any) -> Any:
    resized = cv2.resize(gray_face, (32, 32), interpolation=cv2.INTER_AREA)
    hist = cv2.calcHist([resized], [0], None, [32], [0, 256]).flatten().astype(np.float32)
    pixels = resized.flatten().astype(np.float32) / 255.0
    descriptor = np.concatenate([hist, pixels], axis=0)
    return _normalize_embedding(descriptor)


def _square_box(x: float, y: float, w: float, h: float, frame_w: float, frame_h: float, *, pad_ratio: float = 0.18) -> tuple[int, int, int, int]:
    side = max(float(w), float(h))
    side = side * (1.0 + max(0.0, pad_ratio))
    cx = float(x) + float(w) / 2.0
    cy = float(y) + float(h) / 2.0
    sx = cx - side / 2.0
    sy = cy - side / 2.0
    max_x = max(0.0, float(frame_w) - side)
    max_y = max(0.0, float(frame_h) - side)
    sx = max(0.0, min(max_x, sx))
    sy = max(0.0, min(max_y, sy))
    side = max(1.0, min(side, float(frame_w), float(frame_h)))
    return int(round(sx)), int(round(sy)), int(round(side)), int(round(side))


class FaceRecognitionEngine:
    """Detect faces in media thumbnails and cluster recurring faces."""

    def __init__(self, *, timeout_seconds: float = 6.0, max_images: int = 140) -> None:
        self.timeout_seconds = max(1.0, float(timeout_seconds))
        self.max_images = max(1, int(max_images))
        self._cache: dict[str, dict[str, Any]] = {}
        self._insight_app: Any = None
        self._opencv_detector: Any = None

    @property
    def is_available(self) -> bool:
        return np is not None and (insightface is not None or cv2 is not None)

    def _backend_name(self) -> str:
        if self._get_insight_app() is not None:
            return "insightface_arcface"
        if self._get_opencv_detector() is not None:
            return "opencv_fallback"
        return "unavailable"

    def _get_insight_app(self) -> Any:
        if np is None or insightface is None:
            return None
        if self._insight_app is not None:
            return self._insight_app
        try:
            model_root = Path(os.environ.get("PANOPTO_INSIGHTFACE_HOME", "/tmp/panopto_insightface_models")).resolve()
            model_root.mkdir(parents=True, exist_ok=True)
            os.environ.setdefault("INSIGHTFACE_HOME", str(model_root))
            app = insightface.app.FaceAnalysis(name="buffalo_l", root=str(model_root), providers=["CPUExecutionProvider"])
            app.prepare(ctx_id=0, det_size=(640, 640))
            self._insight_app = app
            return app
        except Exception:
            return None

    def _get_opencv_detector(self) -> Any:
        if np is None or cv2 is None:
            return None
        if self._opencv_detector is not None:
            return self._opencv_detector
        cascade_path = getattr(cv2.data, "haarcascades", "") + "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(cascade_path)
        if detector.empty():
            return None
        self._opencv_detector = detector
        return detector

    def _fetch_frame(self, image_url: str) -> tuple[Any, int, int] | tuple[None, int, int]:
        try:
            response = requests.get(
                image_url,
                timeout=self.timeout_seconds,
                headers={"User-Agent": "PANOPTO/1.0 face-analysis"},
            )
            response.raise_for_status()
            raw = response.content
        except Exception:
            return None, 0, 0
        data = np.frombuffer(raw, dtype=np.uint8)
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR) if cv2 is not None else None
        if frame is None:
            return None, 0, 0
        height, width = frame.shape[:2]
        return frame, int(width), int(height)

    def _prepare_working_frame(self, frame: Any) -> tuple[Any, float]:
        if cv2 is None:
            return frame, 1.0
        h, w = frame.shape[:2]
        longest = max(w, h)
        if longest <= 0:
            return frame, 1.0
        scale = 1.0
        if longest < 480:
            scale = 480.0 / float(longest)
        elif longest > 1280:
            scale = 1280.0 / float(longest)
        if abs(scale - 1.0) < 1e-3:
            return frame, 1.0
        new_w = max(1, int(round(w * scale)))
        new_h = max(1, int(round(h * scale)))
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_CUBIC if scale > 1 else cv2.INTER_AREA)
        return resized, float(scale)

    def _analyze_with_insightface(self, frame: Any, *, scale: float) -> list[dict[str, Any]]:
        app = self._get_insight_app()
        if app is None:
            return []
        try:
            faces = app.get(frame)
        except Exception:
            return []
        rows: list[dict[str, Any]] = []
        for face in faces or []:
            bbox = getattr(face, "bbox", None)
            emb = getattr(face, "embedding", None)
            if bbox is None or emb is None:
                continue
            x1, y1, x2, y2 = [float(v) for v in bbox[:4]]
            w = max(1.0, x2 - x1)
            h = max(1.0, y2 - y1)
            sx, sy, sw, sh = _square_box(x1, y1, w, h, frame.shape[1], frame.shape[0], pad_ratio=0.16)
            inv = 1.0 / max(scale, 1e-6)
            rows.append(
                {
                    "x": max(0, int(round(sx * inv))),
                    "y": max(0, int(round(sy * inv))),
                    "w": max(1, int(round(sw * inv))),
                    "h": max(1, int(round(sh * inv))),
                    "descriptor": _normalize_embedding(emb),
                    "confidence": float(getattr(face, "det_score", 0.85) or 0.85),
                }
            )
        return rows

    def _analyze_with_opencv_fallback(self, frame: Any, *, scale: float) -> list[dict[str, Any]]:
        detector = self._get_opencv_detector()
        if detector is None:
            return []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24))
        rows: list[dict[str, Any]] = []
        inv = 1.0 / max(scale, 1e-6)
        for (x, y, w, h) in detected:
            crop = gray[max(0, y) : max(0, y) + max(1, h), max(0, x) : max(0, x) + max(1, w)]
            if crop.size <= 0:
                continue
            sx, sy, sw, sh = _square_box(float(x), float(y), float(w), float(h), frame.shape[1], frame.shape[0], pad_ratio=0.18)
            rows.append(
                {
                    "x": max(0, int(round(sx * inv))),
                    "y": max(0, int(round(sy * inv))),
                    "w": max(1, int(round(sw * inv))),
                    "h": max(1, int(round(sh * inv))),
                    "descriptor": _opencv_fallback_descriptor(crop),
                    "confidence": float(min(0.98, max(0.35, math.sqrt((w * h) / max(1, frame.shape[0] * frame.shape[1])) * 2.9))),
                }
            )
        return rows

    def _analyze_image(self, image_url: str, *, force_refresh: bool = False) -> dict[str, Any]:
        if image_url in self._cache and not force_refresh:
            return self._cache[image_url]

        if np is None or cv2 is None:
            out = {"faces": [], "error": "numpy_or_opencv_unavailable"}
            self._cache[image_url] = out
            return out

        frame, width, height = self._fetch_frame(image_url)
        if frame is None or width <= 0 or height <= 0:
            out = {"faces": [], "error": "fetch_or_decode_failed"}
            self._cache[image_url] = out
            return out

        working, scale = self._prepare_working_frame(frame)
        faces = self._analyze_with_insightface(working, scale=scale)
        backend = "insightface_arcface"
        if not faces:
            faces = self._analyze_with_opencv_fallback(working, scale=scale)
            backend = "opencv_fallback"

        out = {"faces": faces, "width": width, "height": height, "backend": backend}
        self._cache[image_url] = out
        return out

    def annotate_posts(self, posts: list[dict[str, Any]], *, force_refresh: bool = False) -> dict[str, Any]:
        rows = [dict(item) for item in (posts or []) if isinstance(item, dict)]
        if not rows:
            return {
                "posts": [],
                "face_clusters": [],
                "face_recognition": {"available": self.is_available, "reason": "no_posts", "backend": self._backend_name()},
            }
        if not self.is_available:
            return {
                "posts": rows,
                "face_clusters": [],
                "face_recognition": {"available": False, "reason": "no_supported_backend", "backend": "unavailable"},
            }

        references: list[dict[str, Any]] = []
        analysis_urls: dict[str, bool] = {}
        for post_index, post in enumerate(rows):
            for candidate in _media_candidates(post):
                references.append(
                    {
                        "post_index": post_index,
                        "media_url": candidate.media_url,
                        "analysis_url": candidate.analysis_url,
                    }
                )
                analysis_urls[candidate.analysis_url] = True
        unique_urls = list(analysis_urls.keys())[: self.max_images]

        analyses: dict[str, dict[str, Any]] = {}
        for url in unique_urls:
            analyses[url] = self._analyze_image(url, force_refresh=force_refresh)

        instances: list[dict[str, Any]] = []
        analysis_errors = 0
        backend_used = ""
        for ref in references:
            analyzed = analyses.get(ref["analysis_url"])
            if not analyzed:
                continue
            width = int(analyzed.get("width") or 0)
            height = int(analyzed.get("height") or 0)
            backend_used = str(analyzed.get("backend") or backend_used or "")
            if width <= 0 or height <= 0:
                if analyzed.get("error"):
                    analysis_errors += 1
                continue
            for face in analyzed.get("faces") or []:
                descriptor = face.get("descriptor")
                if descriptor is None:
                    continue
                x = int(face.get("x") or 0)
                y = int(face.get("y") or 0)
                w = int(face.get("w") or 0)
                h = int(face.get("h") or 0)
                if w <= 0 or h <= 0:
                    continue
                instances.append(
                    {
                        "post_index": int(ref["post_index"]),
                        "media_url": str(ref["media_url"]),
                        "analysis_url": str(ref["analysis_url"]),
                        "bbox": {"x": x, "y": y, "w": w, "h": h},
                        "width": width,
                        "height": height,
                        "descriptor": descriptor,
                        "confidence": float(face.get("confidence") or 0.6),
                    }
                )

        threshold = 0.42 if backend_used == "insightface_arcface" else 0.82
        clusters: list[dict[str, Any]] = []
        for item in instances:
            descriptor = item["descriptor"]
            assigned = None
            best_score = -1.0
            for idx, cluster in enumerate(clusters):
                score = _cosine_similarity(descriptor, cluster["centroid"])
                if score >= threshold and score > best_score:
                    assigned = idx
                    best_score = score
            if assigned is None:
                clusters.append({"centroid": descriptor.copy(), "faces": [item]})
            else:
                cluster = clusters[assigned]
                cluster["faces"].append(item)
                stacked = np.stack([face["descriptor"] for face in cluster["faces"]], axis=0)
                cluster["centroid"] = _normalize_embedding(np.mean(stacked, axis=0))

        # Keep recurring identities only.
        ranked = [cluster for cluster in sorted(clusters, key=lambda item: len(item["faces"]), reverse=True) if len(cluster["faces"]) >= 2]
        cluster_entries: list[dict[str, Any]] = []
        cluster_map: dict[int, dict[str, str]] = {}
        for idx, cluster in enumerate(ranked):
            person_id = f"person_{idx + 1}"
            label = f"Person {idx + 1}"
            color = _PERSON_COLORS[idx % len(_PERSON_COLORS)]
            confidences = [float(face.get("confidence") or 0.0) for face in cluster["faces"]]
            avg_confidence = float(sum(confidences) / len(confidences)) if confidences else 0.0
            cluster_entries.append(
                {
                    "person_id": person_id,
                    "label": label,
                    "count": len(cluster["faces"]),
                    "color": color,
                    "avg_confidence": avg_confidence,
                }
            )
            cluster_map[id(cluster)] = {"person_id": person_id, "label": label, "color": color}

        post_face_ids: dict[int, set[str]] = {}
        for post in rows:
            metadata = post.get("metadata")
            if not isinstance(metadata, dict):
                metadata = {}
                post["metadata"] = metadata
            metadata["face_recognition"] = []

        for cluster in ranked:
            mapping = cluster_map.get(id(cluster)) or {}
            person_id = mapping.get("person_id", "")
            label = mapping.get("label", "")
            color = mapping.get("color", "#22c55e")
            for item in cluster["faces"]:
                post_index = int(item["post_index"])
                if post_index < 0 or post_index >= len(rows):
                    continue
                post = rows[post_index]
                metadata = post.get("metadata") if isinstance(post.get("metadata"), dict) else {}
                records = metadata.get("face_recognition") if isinstance(metadata.get("face_recognition"), list) else []
                match = next(
                    (
                        row
                        for row in records
                        if isinstance(row, dict)
                        and str(row.get("media_url") or "") == item["media_url"]
                        and str(row.get("analysis_url") or "") == item["analysis_url"]
                    ),
                    None,
                )
                if not isinstance(match, dict):
                    match = {"media_url": item["media_url"], "analysis_url": item["analysis_url"], "faces": []}
                    records.append(match)
                norm_box = {
                    "x": max(0.0, min(1.0, item["bbox"]["x"] / item["width"])),
                    "y": max(0.0, min(1.0, item["bbox"]["y"] / item["height"])),
                    "w": max(0.0, min(1.0, item["bbox"]["w"] / item["width"])),
                    "h": max(0.0, min(1.0, item["bbox"]["h"] / item["height"])),
                }
                faces = match.get("faces")
                if not isinstance(faces, list):
                    faces = []
                    match["faces"] = faces
                faces.append(
                    {
                        "person_id": person_id,
                        "label": label,
                        "color": color,
                        "bbox": norm_box,
                        "confidence": float(item.get("confidence") or 0.6),
                    }
                )
                metadata["face_recognition"] = records
                post_face_ids.setdefault(post_index, set()).add(person_id)

        for post_index, person_ids in post_face_ids.items():
            rows[post_index]["face_person_ids"] = sorted(person_ids)

        reason = "ok"
        if unique_urls and analysis_errors == len(unique_urls):
            reason = "analysis_fetch_failed"

        return {
            "posts": rows,
            "face_clusters": cluster_entries,
            "face_recognition": {
                "available": True,
                "reason": reason,
                "backend": backend_used or self._backend_name(),
                "images_analyzed": len(unique_urls),
                "faces_detected": len(instances),
            },
        }
