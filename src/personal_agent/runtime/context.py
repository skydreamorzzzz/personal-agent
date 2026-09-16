from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class RuntimeContext:
    """Process dependencies kept outside AgentState."""

    model: Any = None
    workspace_path: Path | None = None
    runtime_data_path: Path | None = None
    log_path: Path | None = None
    checkpoint_backend: Any = None
    memory_backend: Any = None
    capability_registry: Any = None
    logger: Any = None
