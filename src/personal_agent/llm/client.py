from typing import Any, Protocol


class LLMClient(Protocol):
    def invoke(self, messages: list[dict[str, Any]]) -> dict[str, Any]: ...
