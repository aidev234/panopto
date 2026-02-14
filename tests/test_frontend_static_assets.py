from pathlib import Path


def test_index_uses_local_assets_only():
    html = Path("frontend/static/index.html").read_text(encoding="utf-8")

    assert "http://" not in html
    assert "https://" not in html
    assert "/styles.css" in html
    assert "/app.js" in html
