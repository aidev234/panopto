from panopto.analysis.theme_modeling import _prepare_document, _topic_label


def test_prepare_document_strips_profile_noise_and_handles():
    raw = "Sam Altman @sama · 9h View Profile Building safer AI with @openai profile updates"
    cleaned = _prepare_document(raw, "sama")

    assert "view profile" not in cleaned.lower()
    assert " profile " not in f" {cleaned.lower()} "
    assert "@sama" not in cleaned.lower()
    assert "@openai" not in cleaned.lower()
    assert "building safer ai" in cleaned.lower()


def test_prepare_document_strips_screenshot_share_noise():
    raw = "Model update today 1.8K 428 7.4K 1.0M Screenshot Share"
    cleaned = _prepare_document(raw, "sama")

    assert "screenshot" not in cleaned.lower()
    assert "share" not in cleaned.lower()
    assert "model update" in cleaned.lower()
    assert "today" not in cleaned.lower()


def test_prepare_document_strips_time_and_recency_tokens():
    raw = "Activity spiked 7d ago and 3 days back at 12:30pm today"
    cleaned = _prepare_document(raw, "sama")

    lowered = cleaned.lower()
    assert "7d" not in lowered
    assert "3 days" not in lowered
    assert "12:30pm" not in lowered
    assert "today" not in lowered


def test_topic_label_skips_temporal_tokens():
    label, words = _topic_label([("7d", 0.8), ("today", 0.6), ("breach", 0.4)])
    assert label == "breach"
    assert words == ["breach"]
