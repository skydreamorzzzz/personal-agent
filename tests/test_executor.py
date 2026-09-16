import pytest
import json

from tools.executor import execute_tool


def test_execute_read(tmp_path):
    file = tmp_path / "a.txt"
    file.write_text("hello", encoding="utf-8")

    result = execute_tool("read", {"path": str(file)})

    assert result["type"] == "text"
    assert result["content"] == "hello"


def test_execute_list_directory(tmp_path):
    (tmp_path / "child").mkdir()
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")

    result = json.loads(execute_tool("list_directory", {"path": str(tmp_path)}))

    assert {entry["type"] for entry in result["entries"]} == {"file", "directory"}


def test_execute_unknown_tool():
    with pytest.raises(ValueError, match="Unknown tool: unknown"):
        execute_tool("unknown", {})
