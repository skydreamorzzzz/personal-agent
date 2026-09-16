"""User-message normalization and graph handoff."""

from typing import Any, Mapping

from langchain_core.messages import HumanMessage

from personal_agent.application import Application
from personal_agent.entry.models import UserMessageInput


class EntryInputError(ValueError):
    """Raised when an external user input cannot enter the runtime."""


def normalize_user_message(content: str, source: str) -> UserMessageInput:
    """Validate without rewriting the user's original message content."""

    try:
        return UserMessageInput(content=content, source=source)
    except ValueError as exc:
        raise EntryInputError(str(exc)) from exc


def normalize_web_message(payload: Mapping[str, Any]) -> UserMessageInput:
    """Normalize a minimal web-shaped payload without starting a web server."""

    if not isinstance(payload, Mapping) or "text" not in payload:
        raise EntryInputError("Web payload must contain text")
    return normalize_user_message(payload["text"], "web")


def normalize_mobile_message(content: str) -> UserMessageInput:
    """Normalize a mobile message using the shared user contract."""

    return normalize_user_message(content, "mobile")


def submit_user_message(
    application: Application, user_input: UserMessageInput
) -> dict[str, Any]:
    """Inject one HumanMessage and invoke the already-built graph."""

    if not isinstance(user_input, UserMessageInput):
        raise EntryInputError("submit_user_message requires UserMessageInput")

    return application.graph.invoke({"messages": [HumanMessage(content=user_input.content)]})
