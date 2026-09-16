from langchain_core.messages import AIMessage, SystemMessage
from langgraph.runtime import Runtime

from personal_agent.runtime.context import RuntimeContext
from personal_agent.runtime.state import AgentState


SYSTEM_PROMPT = "You are a personal assistant. Answer the user's request clearly and accurately."


class AgentRuntimeError(RuntimeError):
    """Raised when the Agent cannot call its configured model."""


def agent(state: AgentState, runtime: Runtime[RuntimeContext]) -> dict:
    """Call the RuntimeContext model and return one message update."""

    if runtime.context is None or runtime.context.model is None:
        raise AgentRuntimeError("No chat model is configured in RuntimeContext")
    model = runtime.context.model

    model_input = [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]
    response = model.invoke(model_input)
    if not isinstance(response, AIMessage):
        raise AgentRuntimeError("Configured chat model did not return an AIMessage")

    return {"messages": [response], "route": "finalize"}
