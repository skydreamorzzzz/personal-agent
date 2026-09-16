from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from personal_agent.domain.action import ActionProposal
from personal_agent.domain.artifact import Artifact
from personal_agent.domain.task import Task, TaskStatus


class AgentState(TypedDict, total=False):
    """Minimal task-changing state; runtime dependencies do not belong here."""

    messages: Annotated[list[AnyMessage], add_messages]
    task: Task | None
    artifacts: list[Artifact]
    pending_action: ActionProposal | None
    status: TaskStatus
    route: str
