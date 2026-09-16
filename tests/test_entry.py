from dataclasses import dataclass

import pytest
from langchain_core.messages import HumanMessage, SystemMessage

from personal_agent.entry.events import (
    EntryInputError as EventInputError,
    normalize_background_event,
)
from personal_agent.entry.models import BackgroundEventInput, UserMessageInput
from personal_agent.entry.user import (
    EntryInputError,
    normalize_mobile_message,
    normalize_user_message,
    normalize_web_message,
    submit_user_message,
)
from personal_agent.runtime.state import AgentState


def test_user_message_preserves_content_and_source():
    value = "  keep this exact text  "
    message = normalize_user_message(value, "cli")

    assert isinstance(message, UserMessageInput)
    assert message.content == value
    assert message.source == "cli"


@pytest.mark.parametrize("content", ["", "   "])
def test_empty_user_message_is_rejected(content):
    with pytest.raises(EntryInputError):
        normalize_user_message(content, "cli")


def test_cli_web_mobile_share_user_contract():
    assert normalize_user_message("hello", "cli").source == "cli"
    assert normalize_web_message({"text": "hello"}).source == "web"
    assert normalize_mobile_message("hello").source == "mobile"


def test_user_message_becomes_human_message_without_system_message():
    seen = {}

    class FakeGraph:
        def invoke(self, state):
            seen["state"] = state
            return {"status": "completed"}

    @dataclass
    class FakeApplication:
        graph: object

    result = submit_user_message(
        FakeApplication(FakeGraph()), normalize_user_message("hello", "web")
    )

    assert result == {"status": "completed"}
    messages = seen["state"]["messages"]
    assert len(messages) == 1
    assert isinstance(messages[0], HumanMessage)
    assert not any(isinstance(message, SystemMessage) for message in messages)


def test_agent_state_uses_add_messages_annotation():
    messages = AgentState.__annotations__["messages"]
    assert "add_messages" in str(messages)


def test_background_event_stays_structured_and_not_human_message():
    event = normalize_background_event(
        "new_mail", "mail", {"message_id": "opaque-id"}
    )

    assert isinstance(event, BackgroundEventInput)
    assert event.payload["message_id"] == "opaque-id"
    assert not isinstance(event, HumanMessage)


def test_malformed_background_event_is_rejected():
    with pytest.raises(EventInputError):
        normalize_background_event("", "mail", {})
    with pytest.raises(EventInputError):
        normalize_background_event("new_mail", "mail", [])


def test_web_payload_requires_text():
    with pytest.raises(EntryInputError):
        normalize_web_message({})


def test_entry_does_not_bootstrap_application(monkeypatch):
    def fail_bootstrap(*args, **kwargs):
        raise AssertionError("Entry must not bootstrap")

    monkeypatch.setattr("personal_agent.bootstrap.bootstrap_application", fail_bootstrap)
    assert normalize_user_message("no bootstrap", "cli").content == "no bootstrap"
