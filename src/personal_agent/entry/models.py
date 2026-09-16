"""Normalized inputs accepted at the external-world boundary."""

from dataclasses import dataclass
from typing import Any, Mapping


USER_MESSAGE_SOURCES = {"cli", "web", "mobile"}


@dataclass(frozen=True)
class UserMessageInput:
    """A user-authored message normalized from an Entry adapter."""

    content: str
    source: str

    def __post_init__(self) -> None:
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("User message content must be a non-empty string")
        if self.source not in USER_MESSAGE_SOURCES:
            raise ValueError(f"Unsupported user message source: {self.source}")


@dataclass(frozen=True)
class BackgroundEventInput:
    """A structured external event, kept separate from user messages."""

    event_type: str
    source: str
    payload: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.event_type, str) or not self.event_type.strip():
            raise ValueError("Background event_type must be a non-empty string")
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("Background event source must be a non-empty string")
        if not isinstance(self.payload, Mapping):
            raise ValueError("Background event payload must be a mapping")
