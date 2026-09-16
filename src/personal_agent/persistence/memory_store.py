from typing import Any, Protocol


class MemoryStore(Protocol):
    def retrieve(self, query: str) -> list[Any]: ...

    def write(self, item: Any) -> None: ...
