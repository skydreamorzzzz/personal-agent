from personal_agent.runtime.state import AgentState


def tool_dispatch(state: AgentState) -> dict:
    """Placeholder capability dispatch boundary; no tool is active."""

    return {"route": "finalize"}
