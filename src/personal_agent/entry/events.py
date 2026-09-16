"""Background-event normalization; runtime integration is intentionally absent."""

from typing import Any, Mapping

from personal_agent.entry.models import BackgroundEventInput


class EntryInputError(ValueError):
    """Raised when an external event cannot be normalized."""


def normalize_background_event(
    event_type: str, source: str, payload: Mapping[str, Any]
) -> BackgroundEventInput:
    """Validate a structured event without converting it to a user message."""

    try:
        return BackgroundEventInput(
            event_type=event_type,
            source=source,
            payload=payload,
        )
    except ValueError as exc:
        raise EntryInputError(str(exc)) from exc
