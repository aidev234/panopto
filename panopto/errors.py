"""Shared domain errors for collection and workflow operations."""

from __future__ import annotations


class UsernameNotFoundError(ValueError):
    """Raised when a requested account is not found on a source platform."""

    def __init__(self, platform: str, username: str):
        self.platform = platform
        self.username = username
        super().__init__(f"{platform} username '{username}' not found")
