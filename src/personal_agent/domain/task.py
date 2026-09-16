from dataclasses import dataclass
from typing import Literal

TaskStatus = Literal["running", "waiting_user", "completed", "failed"]


@dataclass
class Task:
    id: str
    intent: str
    status: TaskStatus = "running"
