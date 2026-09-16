from dataclasses import dataclass
from pathlib import Path

from langchain_core.language_models import BaseChatModel


@dataclass
class RuntimeContext:
    """Process dependencies kept outside AgentState."""

    model: BaseChatModel | None = None
    workspace_path: Path | None = None
    runtime_data_path: Path | None = None
    log_path: Path | None = None
    checkpoint_backend: object | None = None
    memory_backend: object | None = None
    capability_registry: object | None = None
    logger: object | None = None
