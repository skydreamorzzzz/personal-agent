"""Small provider boundary for constructing the configured chat model."""

import os
from pathlib import Path
from typing import Callable

from langchain_core.language_models import BaseChatModel
from langchain_deepseek import ChatDeepSeek

from personal_agent.config.models import LLMConfig


class LLMConfigurationError(ValueError):
    """Raised when the configured model or credential cannot be constructed."""


def _read_api_key(config: LLMConfig) -> str:
    credential = config.credential
    if credential.source == "env":
        if not credential.env_name:
            raise LLMConfigurationError("Missing credential environment variable name")
        value = os.environ.get(credential.env_name)
        if not value or not value.strip():
            raise LLMConfigurationError(
                f"Missing required environment variable: {credential.env_name}"
            )
        return value.strip()

    if credential.source == "file":
        path: Path | None = credential.path
        if path is None:
            raise LLMConfigurationError("Missing credential file path")
        try:
            value = path.read_text(encoding="utf-8").strip()
        except FileNotFoundError as exc:
            raise LLMConfigurationError("Configured credential file does not exist") from exc
        except OSError as exc:
            raise LLMConfigurationError("Unable to read configured credential file") from exc
        if not value:
            raise LLMConfigurationError("Configured credential file is empty")
        return value

    raise LLMConfigurationError("Unsupported credential source")


def build_chat_model(config: LLMConfig) -> BaseChatModel:
    """Construct the one currently supported provider without binding tools."""

    if config.provider != "deepseek":
        raise LLMConfigurationError(
            f"Unsupported LLM provider: {config.provider}"
        )

    api_key = _read_api_key(config)
    kwargs: dict[str, object] = {
        "model": config.model,
        "api_key": api_key,
    }
    if config.endpoint is not None:
        kwargs["base_url"] = config.endpoint
    return ChatDeepSeek(**kwargs)


ModelFactory = Callable[[LLMConfig], BaseChatModel]
