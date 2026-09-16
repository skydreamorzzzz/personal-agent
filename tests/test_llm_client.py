import json
from types import SimpleNamespace

from llm.client import _convert_response


def test_convert_response_preserves_tool_call_id():
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    tool_calls=[
                        SimpleNamespace(
                            id="call_test_123",
                            function=SimpleNamespace(
                                name="read",
                                arguments=json.dumps({"path": "README.md"}),
                            ),
                        )
                    ]
                )
            )
        ]
    )

    assert _convert_response(response) == {
        "type": "tool_call",
        "id": "call_test_123",
        "name": "read",
        "arguments": {"path": "README.md"},
    }
