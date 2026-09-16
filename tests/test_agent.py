from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.runtime import Runtime

from personal_agent.bootstrap import bootstrap_application
from personal_agent.entry.user import normalize_user_message, submit_user_message
from personal_agent.runtime.context import RuntimeContext
from personal_agent.runtime.nodes.agent import AgentRuntimeError, agent


class RecordingModel:
    def __init__(self):
        self.calls = []

    def invoke(self, messages):
        self.calls.append(messages)
        return AIMessage(content="fake answer")


def test_agent_uses_runtime_context_model_and_temporary_system_message():
    model = RecordingModel()
    state = {"messages": [HumanMessage(content="hello")]}

    update = agent(state, Runtime(context=RuntimeContext(model=model)))

    assert isinstance(update["messages"][0], AIMessage)
    assert update["messages"][0].content == "fake answer"
    assert update["route"] == "finalize"
    assert len(model.calls) == 1
    assert isinstance(model.calls[0][0], SystemMessage)
    assert isinstance(model.calls[0][1], HumanMessage)
    assert model.calls[0][1].content == "hello"
    assert state["messages"] == [state["messages"][0]]


def test_agent_model_none_has_clear_error():
    try:
        agent(
            {"messages": [HumanMessage(content="hello")]},
            Runtime(context=RuntimeContext()),
        )
    except AgentRuntimeError as error:
        assert str(error) == "No chat model is configured in RuntimeContext"
    else:
        raise AssertionError("agent should reject a missing model")


def test_real_graph_entry_to_fake_model_keeps_system_message_out_of_state():
    model = RecordingModel()
    application = bootstrap_application(model_factory=lambda config: model)

    result = submit_user_message(
        application, normalize_user_message("hello", "cli")
    )

    assert [type(message) for message in result["messages"]] == [
        HumanMessage,
        AIMessage,
    ]
    assert result["messages"][0].content == "hello"
    assert result["messages"][1].content == "fake answer"
    assert result["status"] == "completed"
    assert isinstance(model.calls[0][0], SystemMessage)
