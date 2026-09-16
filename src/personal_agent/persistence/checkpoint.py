from typing import Any, Protocol


class CheckpointBackend(Protocol):
    def save(self, task_id: str, state: dict[str, Any]) -> None: ...

    def load(self, task_id: str) -> dict[str, Any] | None: ...


def build_checkpoint_backend() -> CheckpointBackend:
    raise NotImplementedError("Checkpoint backend is not implemented in v0.1")
