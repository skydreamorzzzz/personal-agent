import json
from datetime import datetime
from pathlib import Path


def _create_trajectory_log():
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    return logs_dir / f"react-{timestamp}.jsonl"


def _write_event(log_path, event):
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(event, ensure_ascii=False) + "\n")


def _user_input(messages):
    for message in reversed(messages):
        if message.get("role") == "user":
            return message.get("content")
    return None


def react(
    planned_input,
    call_llm,
    execute_tool,
    tools,
    max_steps=10,
):
    messages = list(planned_input)
    log_path = _create_trajectory_log()
    _write_event(log_path, {"event": "run_start", "input": _user_input(messages)})

    try:
        for step in range(1, max_steps + 1):
            response = call_llm(messages, tools)
            response_type = response.get("type")

            if response_type == "final":
                _write_event(
                    log_path,
                    {
                        "event": "final",
                        "step": step,
                        "content": response.get("content"),
                    },
                )
                return response.get("content")

            if response_type == "tool_call":
                tool_name = response.get("name")
                arguments = response.get("arguments", {})
                tool_call_id = response["id"]
                _write_event(
                    log_path,
                    {
                        "event": "tool_call",
                        "step": step,
                        "id": tool_call_id,
                        "name": tool_name,
                        "arguments": arguments,
                    },
                )
                observation = execute_tool(tool_name, arguments)
                observation_content = (
                    observation if isinstance(observation, str) else str(observation)
                )
                _write_event(
                    log_path,
                    {
                        "event": "tool_result",
                        "step": step,
                        "tool_call_id": tool_call_id,
                        "content": observation_content,
                    },
                )

                messages.append(
                    {
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": tool_call_id,
                                "type": "function",
                                "function": {
                                    "name": tool_name,
                                    "arguments": json.dumps(
                                        arguments, ensure_ascii=False
                                    ),
                                },
                            }
                        ],
                    }
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": observation_content,
                    }
                )
                continue

            raise ValueError("Unsupported LLM response type")

        error = RuntimeError("ReAct reached max_steps without a final answer")
        _write_event(
            log_path,
            {
                "event": "error",
                "error_type": "max_steps",
                "message": str(error),
            },
        )
        raise error
    except Exception as error:
        if not (
            isinstance(error, RuntimeError)
            and str(error) == "ReAct reached max_steps without a final answer"
        ):
            _write_event(
                log_path,
                {
                    "event": "error",
                    "error_type": type(error).__name__,
                    "message": str(error),
                },
            )
        raise
