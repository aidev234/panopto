from theme_modeling import _prepare_document


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
    assert "model update today" in cleaned.lower()
