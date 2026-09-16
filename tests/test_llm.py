import pytest

from personal_agent.config.models import CredentialConfig, LLMConfig
from personal_agent.llm import client
from personal_agent.llm.client import LLMConfigurationError, build_chat_model


def env_config(endpoint=None):
    return LLMConfig(
        provider="deepseek",
        model="deepseek-chat",
        credential=CredentialConfig(source="env", env_name="TEST_DEEPSEEK_KEY"),
        endpoint=endpoint,
    )


def test_build_chat_model_reads_env_and_passes_endpoint(monkeypatch):
    received = {}

    class FakeChatDeepSeek:
        def __init__(self, **kwargs):
            received.update(kwargs)

    monkeypatch.setenv("TEST_DEEPSEEK_KEY", "fake-value")
    monkeypatch.setattr(client, "ChatDeepSeek", FakeChatDeepSeek)

    result = build_chat_model(env_config("https://example.invalid"))

    assert isinstance(result, FakeChatDeepSeek)
    assert received == {
        "model": "deepseek-chat",
        "api_key": "fake-value",
        "base_url": "https://example.invalid",
    }


def test_missing_env_credential_is_clear_and_secret_free(monkeypatch):
    monkeypatch.delenv("TEST_DEEPSEEK_KEY", raising=False)

    with pytest.raises(LLMConfigurationError) as error:
        build_chat_model(env_config())

    assert "TEST_DEEPSEEK_KEY" in str(error.value)
    assert "fake-value" not in str(error.value)


def test_file_credential_is_stripped(monkeypatch, tmp_path):
    credential_path = tmp_path / "API.txt"
    credential_path.write_text("  fake-file-key\n", encoding="utf-8")
    config = LLMConfig(
        provider="deepseek",
        model="deepseek-chat",
        credential=CredentialConfig(source="file", path=credential_path),
    )
    received = {}

    class FakeChatDeepSeek:
        def __init__(self, **kwargs):
            received.update(kwargs)

    monkeypatch.setattr(client, "ChatDeepSeek", FakeChatDeepSeek)
    build_chat_model(config)

    assert received["api_key"] == "fake-file-key"


def test_empty_file_credential_is_rejected(tmp_path):
    credential_path = tmp_path / "API.txt"
    credential_path.write_text(" \n", encoding="utf-8")
    config = LLMConfig(
        provider="deepseek",
        model="deepseek-chat",
        credential=CredentialConfig(source="file", path=credential_path),
    )

    with pytest.raises(LLMConfigurationError, match="empty"):
        build_chat_model(config)
