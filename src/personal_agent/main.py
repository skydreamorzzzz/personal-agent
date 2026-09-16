"""Entry point helpers for the architecture scaffold."""

from personal_agent.runtime.builder import build_graph


def create_runtime_graph():
    """Build the safe, side-effect-free v0.1 graph."""

    return build_graph()
