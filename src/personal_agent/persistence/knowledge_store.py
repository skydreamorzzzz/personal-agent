from typing import Any, Protocol


class KnowledgeStore(Protocol):
    def put(self, source: str, content: Any, metadata: dict[str, Any]) -> None: ...

    def find(self, query: str) -> list[Any]: ...
