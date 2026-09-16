from dataclasses import dataclass
from typing import Literal

ApprovalDecision = Literal["approve", "reject", "edit", "clarify"]


@dataclass
class ApprovalRequest:
    action_id: str
    summary: str
    consequences: str


class ApprovalHandler:
    """Interface shape for a future UI or LangGraph interrupt/resume adapter."""

    def decide(self, request: ApprovalRequest) -> ApprovalDecision:
        raise NotImplementedError
