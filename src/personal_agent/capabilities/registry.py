from typing import Any

from personal_agent.capabilities.base import Capability


class CapabilityRegistry:
    """Small explicit registry; no placeholder capability is registered."""

    def __init__(self) -> None:
        self._capabilities: dict[str, Capability] = {}

    def register(self, capability: Capability) -> None:
        self._capabilities[capability.name] = capability

    def get(self, name: str) -> Capability | None:
        return self._capabilities.get(name)

    def schemas(self) -> list[dict[str, Any]]:
        return [capability.describe() for capability in self._capabilities.values()]
