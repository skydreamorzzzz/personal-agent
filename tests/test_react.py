import json

import pytest

from agent.react import react


def test_react_writes_matching_tool_call_id():
    responses = iter(
        [
            {
                "type": "tool_call",
                "id": "call_test_123",
                "name": "read",
                "arguments": {"path": "README.md"},
            },
            {"type": "final", "content": "读取完成"},
        ]
    )
    calls = []

    def call_llm(messages, tools):
        calls.append(messages)
        return next(responses)

    def execute_tool(tool_name, arguments):
        assert tool_name == "read"
        assert arguments == {"path": "README.md"}
        return {"type": "text", "content": "hello"}

    result = react(
        planned_input=[{"role": "user", "content": "读取 README.md"}],
        call_llm=call_llm,
        execute_tool=execute_tool,
        tools=[],
    )

    assert result == "读取完成"
    second_messages = calls[1]
    assert second_messages[-2] == {
        "role": "assistant",
        "tool_calls": [
            {
                "id": "call_test_123",
                "type": "function",
                "function": {
                    "name": "read",
                    "arguments": '{"path": "README.md"}',
                },
            }
        ],
    }
    assert second_messages[-1] == {
        "role": "tool",
        "tool_call_id": "call_test_123",
        "content": "{'type': 'text', 'content': 'hello'}",
    }


def test_react_writes_jsonl_trajectory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    responses = iter(
        [
            {
                "type": "tool_call",
                "id": "call_log_123",
                "name": "read",
                "arguments": {"path": "README.md"},
            },
            {"type": "final", "content": "完成"},
        ]
    )

    result = react(
        planned_input=[{"role": "user", "content": "读取文件"}],
        call_llm=lambda messages, tools: next(responses),
        execute_tool=lambda name, arguments: "内容",
        tools=[],
    )

    assert result == "完成"
    log_path = next((tmp_path / "logs").glob("react-*.jsonl"))
    events = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    assert events[0] == {"event": "run_start", "input": "读取文件"}
    assert events[1]["event"] == "tool_call"
    assert events[1]["id"] == "call_log_123"
    assert events[2] == {
        "event": "tool_result",
        "step": 1,
        "tool_call_id": "call_log_123",
        "content": "内容",
    }
    assert events[3] == {"event": "final", "step": 2, "content": "完成"}


def test_react_logs_max_steps_error(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with pytest.raises(RuntimeError, match="max_steps"):
        react(
            planned_input=[{"role": "user", "content": "继续"}],
            call_llm=lambda messages, tools: {
                "type": "tool_call",
                "id": "call_loop",
                "name": "read",
                "arguments": {"path": "README.md"},
            },
            execute_tool=lambda name, arguments: "内容",
            tools=[],
            max_steps=1,
        )

    log_path = next((tmp_path / "logs").glob("react-*.jsonl"))
    events = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    assert events[-1]["event"] == "error"
    assert events[-1]["error_type"] == "max_steps"
