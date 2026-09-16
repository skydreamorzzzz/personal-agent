from typing import Any, Protocol


class MemoryReflector(Protocol):
    def reflect(self, task: Any) -> list[Any]: ...
