"""Shared domain errors for collection and workflow operations."""

from __future__ import annotations


class UsernameNotFoundError(ValueError):
    """Raised when a requested account is not found on a source platform."""

    def __init__(self, platform: str, username: str):
        self.platform = platform
        self.username = username
        super().__init__(f"{platform} username '{username}' not found")


class SourceAccessBlockedError(RuntimeError):
    """Raised when a source is blocked by anti-bot/challenge protections."""

    def __init__(self, platform: str, username: str, reason: str = "blocked_by_protection"):
        self.platform = platform
        self.username = username
        self.reason = reason
        super().__init__(f"{platform} access blocked for username '{username}' ({reason})")
