"""Minimal colorama compatibility shim for vendored user_scanner.

This keeps recon functional in restricted environments where colorama
cannot be installed from PyPI.
"""

from __future__ import annotations


class _Codes:
    BLACK = ""
    RED = ""
    GREEN = ""
    YELLOW = ""
    BLUE = ""
    MAGENTA = ""
    CYAN = ""
    WHITE = ""
    RESET = ""
    RESET_ALL = ""


Fore = _Codes()
Back = _Codes()
Style = _Codes()


def init(*_args, **_kwargs):  # pragma: no cover - compatibility no-op
    return None


def deinit():  # pragma: no cover - compatibility no-op
    return None


def reinit():  # pragma: no cover - compatibility no-op
    return None
