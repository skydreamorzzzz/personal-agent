from personal_agent.runtime.state import AgentState


def memory_retrieve(state: AgentState) -> dict:
    """Placeholder: no memory backend is connected yet."""

    return {"status": state.get("status", "running")}
