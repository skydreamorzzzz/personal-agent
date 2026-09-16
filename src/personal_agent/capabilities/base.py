from typing import Any, Protocol


class Capability(Protocol):
    name: str

    def describe(self) -> dict[str, Any]: ...
