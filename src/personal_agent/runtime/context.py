from dataclasses import dataclass
from typing import Any


@dataclass
class RuntimeContext:
    """Process dependencies kept outside AgentState."""

    model: Any = None
    workspace_path: str | None = None
    checkpoint_backend: Any = None
    memory_backend: Any = None
    capability_registry: Any = None
    logger: Any = None
