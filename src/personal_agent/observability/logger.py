from typing import Any, Protocol


class RuntimeLogger(Protocol):
    def event(self, name: str, **fields: Any) -> None: ...


def log_event(logger: RuntimeLogger | None, name: str, **fields: Any) -> None:
    """Thin hook only; no logging backend or secret redaction is connected yet."""

    if logger is not None:
        logger.event(name, **fields)
