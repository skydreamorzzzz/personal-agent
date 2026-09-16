import json

import pytest

from tools.list_directory import list_directory


def test_list_directory_returns_valid_json_with_files_and_directories(tmp_path):
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "b.py").write_text("pass", encoding="utf-8")
    (tmp_path / "child").mkdir()

    result = json.loads(list_directory(str(tmp_path)))

    assert result["path"] == str(tmp_path)
    assert isinstance(result["entries"], list)
    assert {entry["type"] for entry in result["entries"]} == {"file", "directory"}
    assert {entry["path"] for entry in result["entries"]} == {
        str(tmp_path / "a.txt"),
        str(tmp_path / "b.py"),
        str(tmp_path / "child"),
    }
    assert all(set(entry) == {"path", "type"} for entry in result["entries"])


def test_list_directory_is_not_recursive(tmp_path):
    child = tmp_path / "child"
    child.mkdir()
    (child / "deep.txt").write_text("deep", encoding="utf-8")

    result = json.loads(list_directory(str(tmp_path)))
    paths = {entry["path"] for entry in result["entries"]}

    assert str(child) in paths
    assert str(child / "deep.txt") not in paths


def test_list_directory_entries_are_sorted(tmp_path):
    (tmp_path / "z.txt").write_text("z", encoding="utf-8")
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")

    result = json.loads(list_directory(str(tmp_path)))

    assert [entry["path"] for entry in result["entries"]] == [
        str(tmp_path / "a.txt"),
        str(tmp_path / "z.txt"),
    ]


def test_list_directory_missing_path(tmp_path):
    with pytest.raises(FileNotFoundError):
        list_directory(str(tmp_path / "missing"))


def test_list_directory_rejects_file(tmp_path):
    file = tmp_path / "file.txt"
    file.write_text("hello", encoding="utf-8")

    with pytest.raises(NotADirectoryError):
        list_directory(str(file))
