from typing import Callable

from personal_agent.application import Application
from personal_agent.entry.user import normalize_user_message, submit_user_message


def run_once(
    application: Application,
    input_fn: Callable[[str], str] = input,
) -> dict:
    """Read one CLI message, submit it, and return the real graph result."""

    user_input = normalize_user_message(input_fn("You: "), "cli")
    return submit_user_message(application, user_input)


def receive_once() -> str:
    """Compatibility placeholder for callers that have no Application yet."""

    raise NotImplementedError("CLI receive_once requires an Application in v0.1")
