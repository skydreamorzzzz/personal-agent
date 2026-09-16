from typing import Literal

from personal_agent.runtime.state import AgentState

AgentRoute = Literal["tool_dispatch", "memory_write", "action_proposal", "finalize"]
ApprovalRoute = Literal["execute_action", "agent"]


def route_after_agent(state: AgentState) -> AgentRoute:
    """Route only from explicit state markers; default is the safe finish path."""

    if state.get("pending_action") is not None:
        return "action_proposal"
    route = state.get("route")
    if route in {"tool_dispatch", "memory_write"}:
        return route
    return "finalize"


def route_after_approval(state: AgentState) -> ApprovalRoute:
    proposal = state.get("pending_action")
    if proposal is not None and proposal.approval_status == "approved":
        return "execute_action"
    return "agent"
