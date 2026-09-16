from dataclasses import dataclass
from typing import Any

from personal_agent.config.models import AppConfig
from personal_agent.runtime.context import RuntimeContext


@dataclass(frozen=True)
class Application:
    """Composed application dependencies, not task state."""

    config: AppConfig
    graph: Any
    context: RuntimeContext
