from __future__ import annotations

import sys

import panopto.__main__ as panopto_main


def test_module_entrypoint_defaults_to_loopback(monkeypatch):
    captured: dict[str, object] = {}

    def _fake_run(*, host: str, port: int) -> None:
        captured["host"] = host
        captured["port"] = port

    monkeypatch.setattr(panopto_main, "run", _fake_run)
    monkeypatch.setattr(sys, "argv", ["panopto"])

    panopto_main.main()

    assert captured == {"host": "127.0.0.1", "port": 8000}
