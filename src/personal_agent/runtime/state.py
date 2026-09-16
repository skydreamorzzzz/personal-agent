from typing import Any, TypedDict

from personal_agent.domain.action import ActionProposal
from personal_agent.domain.artifact import Artifact
from personal_agent.domain.task import Task, TaskStatus


class AgentState(TypedDict, total=False):
    """Minimal task-changing state; runtime dependencies do not belong here."""

    messages: list[dict[str, Any]]
    task: Task | None
    artifacts: list[Artifact]
    pending_action: ActionProposal | None
    status: TaskStatus
    route: str
