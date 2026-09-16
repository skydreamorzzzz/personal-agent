from dataclasses import dataclass, field
from typing import Any


@dataclass
class Artifact:
    kind: str
    identifier: str
    source: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
