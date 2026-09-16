import pytest

from tools.read import UnsupportedFileTypeError, classify_file, read


def test_read_txt(tmp_path):
    path = tmp_path / "note.txt"
    path.write_text("hello", encoding="utf-8")

    assert read(str(path)) == {
        "path": str(path),
        "type": "text",
        "content": "hello",
    }


def test_read_python_file(tmp_path):
    path = tmp_path / "example.py"
    path.write_text("print('hello')", encoding="utf-8")

    result = read(str(path))

    assert result["type"] == "code"
    assert result["content"] == "print('hello')"


def test_classify_extension_is_case_insensitive():
    assert classify_file("README.TXT") == "text"
    assert classify_file("script.PY") == "code"


def test_read_unsupported_file_type(tmp_path):
    path = tmp_path / "image.png"
    path.write_bytes(b"not an image")

    with pytest.raises(UnsupportedFileTypeError):
        read(str(path))


def test_read_missing_file(tmp_path):
    path = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        read(str(path))


def test_read_directory(tmp_path):
    with pytest.raises(IsADirectoryError):
        read(str(tmp_path))
