from dataclasses import dataclass
from typing import Any, Literal

ApprovalStatus = Literal["pending", "approved", "rejected", "edited"]


@dataclass
class ActionProposal:
    action_type: str
    capability: str
    parameters: dict[str, Any]
    summary: str
    consequences: str
    approval_status: ApprovalStatus = "pending"
