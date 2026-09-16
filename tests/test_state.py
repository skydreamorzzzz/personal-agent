from typing import Annotated, TypedDict, get_args

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from personal_agent.bootstrap import bootstrap_application
from personal_agent.runtime.state import AgentState


def test_agent_state_messages_uses_add_messages_reducer():
    annotation = AgentState.__annotations__["messages"]
    annotated_message_type = get_args(annotation)[0]

    assert annotated_message_type.__metadata__ == (add_messages,)


class MessageTestState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def test_add_messages_appends_node_updates_in_order():
    def node_a(state: MessageTestState):
        return {"messages": [AIMessage(content="first")]}

    def node_b(state: MessageTestState):
        return {"messages": [AIMessage(content="second")]}

    graph = StateGraph(MessageTestState)
    graph.add_node("node_a", node_a)
    graph.add_node("node_b", node_b)
    graph.add_edge(START, "node_a")
    graph.add_edge("node_a", "node_b")
    graph.add_edge("node_b", END)

    result = graph.compile().invoke(
        {"messages": [HumanMessage(content="hello")]}
    )

    assert [message.content for message in result["messages"]] == [
        "hello",
        "first",
        "second",
    ]
    assert isinstance(result["messages"][0], HumanMessage)


def test_messages_only_initial_state_runs_current_safe_graph():
    class FakeModel:
        def invoke(self, messages):
            return AIMessage(content="fake response")

    application = bootstrap_application(model_factory=lambda config: FakeModel())

    result = application.graph.invoke(
        {"messages": [HumanMessage(content="hello")]},
        context=application.context,
    )

    assert result["messages"][0].content == "hello"
    assert result["status"] == "completed"


def test_agent_state_does_not_require_runtime_context_dependencies():
    fields = AgentState.__annotations__

    assert "messages" in fields
    assert "model" not in fields
    assert "capability_registry" not in fields
    assert "workspace_path" not in fields
    assert "config" not in fields

    assert AgentState.__required_keys__ == {"messages"}


def test_placeholder_state_fields_are_optional():
    state: AgentState = {"messages": [HumanMessage(content="hello")]}

    assert "task" not in state
    assert "artifacts" not in state
    assert "pending_action" not in state
