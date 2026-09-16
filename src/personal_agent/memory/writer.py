from typing import Any, Protocol


class MemoryWriter(Protocol):
    def write(self, memory: Any) -> None: ...
