from typing import Any, Protocol


class MemoryRetriever(Protocol):
    def retrieve(self, task: Any) -> list[Any]: ...
