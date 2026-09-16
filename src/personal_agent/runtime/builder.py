from langgraph.graph import END, START, StateGraph

from personal_agent.runtime.nodes.action_proposal import action_proposal
from personal_agent.runtime.nodes.agent import agent
from personal_agent.runtime.nodes.approval import approval_gate
from personal_agent.runtime.nodes.execute_action import execute_action
from personal_agent.runtime.nodes.finalize import finalize
from personal_agent.runtime.nodes.memory_reflection import memory_reflection
from personal_agent.runtime.nodes.memory_retrieve import memory_retrieve
from personal_agent.runtime.nodes.memory_write import memory_write
from personal_agent.runtime.nodes.tool_dispatch import tool_dispatch
from personal_agent.runtime.context import RuntimeContext
from personal_agent.runtime.routing import route_after_agent, route_after_approval
from personal_agent.runtime.state import AgentState


def build_graph():
    """Build the v0.1 graph without connecting external side effects."""

    graph = StateGraph(AgentState, context_schema=RuntimeContext)
    graph.add_node("memory_retrieve", memory_retrieve)
    graph.add_node("agent", agent)
    graph.add_node("tool_dispatch", tool_dispatch)
    graph.add_node("memory_write", memory_write)
    graph.add_node("action_proposal", action_proposal)
    graph.add_node("approval_gate", approval_gate)
    graph.add_node("execute_action", execute_action)
    graph.add_node("finalize", finalize)
    graph.add_node("memory_reflection", memory_reflection)

    graph.add_edge(START, "memory_retrieve")
    graph.add_edge("memory_retrieve", "agent")
    graph.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tool_dispatch": "tool_dispatch",
            "memory_write": "memory_write",
            "action_proposal": "action_proposal",
            "finalize": "finalize",
        },
    )
    graph.add_edge("tool_dispatch", "agent")
    graph.add_edge("memory_write", "agent")
    graph.add_edge("action_proposal", "approval_gate")
    graph.add_conditional_edges(
        "approval_gate",
        route_after_approval,
        {"execute_action": "execute_action", "agent": "agent"},
    )
    graph.add_edge("execute_action", "agent")
    graph.add_edge("finalize", "memory_reflection")
    graph.add_edge("memory_reflection", END)
    return graph.compile()
