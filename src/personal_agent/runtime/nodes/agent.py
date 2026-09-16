from personal_agent.runtime.state import AgentState


def agent(state: AgentState) -> dict:
    """Placeholder reasoning node; the safe default is to finish."""

    return {"status": state.get("status", "running"), "route": "finalize"}
