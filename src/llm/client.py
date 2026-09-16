import json
import os
from pathlib import Path

import yaml


_SUPPORTED_PROVIDER = "deepseek"
_SETTINGS_PATH = Path(__file__).resolve().parents[2] / "config" / "settings.yaml"
_client = None
_model = None


def _load_settings():
    try:
        with _SETTINGS_PATH.open(encoding="utf-8") as settings_file:
            settings = yaml.safe_load(settings_file) or {}
    except FileNotFoundError as exc:
        raise ValueError("settings.yaml 不存在") from exc

    llm_settings = settings.get("llm")
    if not isinstance(llm_settings, dict):
        raise ValueError("LLM 配置缺失")

    provider = llm_settings.get("provider")
    model = llm_settings.get("model")
    credential = llm_settings.get("credential")
    if not provider or not model or not isinstance(credential, dict):
        raise ValueError("LLM 必要配置缺失")
    if provider != _SUPPORTED_PROVIDER:
        raise ValueError("不支持的 provider")

    return llm_settings


def _read_credential(credential):
    source = credential.get("source")

    if source == "env":
        env_name = credential.get("env_name")
        if not env_name:
            raise ValueError("环境变量名称缺失")
        api_key = os.environ.get(env_name)
        if not api_key:
            raise ValueError("缺少凭证")
        return api_key

    if source == "file":
        path = credential.get("path")
        if not path:
            raise ValueError("凭证文件路径缺失")
        try:
            with Path(path).open(encoding="utf-8") as credential_file:
                api_key = credential_file.read().strip()
        except FileNotFoundError as exc:
            raise ValueError("凭证文件不存在") from exc
        if not api_key:
            raise ValueError("缺少凭证")
        return api_key

    raise ValueError("credential.source 配置错误")


def _get_client():
    global _client, _model

    if _client is not None:
        return _client, _model

    settings = _load_settings()
    api_key = _read_credential(settings["credential"])

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError("运行 LLM client 需要安装 openai") from exc

    _client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    _model = settings["model"]
    return _client, _model


def _convert_response(response):
    message = response.choices[0].message
    tool_calls = message.tool_calls or []

    if tool_calls:
        tool_call = tool_calls[0]
        try:
            arguments = json.loads(tool_call.function.arguments)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValueError("无法解析 tool arguments") from exc
        if not isinstance(arguments, dict):
            raise ValueError("tool arguments 必须是对象")
        return {
            "type": "tool_call",
            "id": tool_call.id,
            "name": tool_call.function.name,
            "arguments": arguments,
        }

    return {
        "type": "final",
        "content": message.content or "",
    }


def call_llm(messages, tools):
    client, model = _get_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
    )
    return _convert_response(response)
