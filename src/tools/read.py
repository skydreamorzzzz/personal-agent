from pathlib import Path


TEXT_EXTENSIONS = {".txt", ".md", ".log", ".json", ".yaml", ".yml"}
CODE_EXTENSIONS = {".py", ".c", ".cpp", ".h", ".hpp", ".java", ".js", ".ts"}


class UnsupportedFileTypeError(Exception):
    pass


def classify_file(path):
    extension = Path(path).suffix.lower()

    if extension in TEXT_EXTENSIONS:
        return "text"
    if extension in CODE_EXTENSIONS:
        return "code"
    return "unsupported"


def read_text(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def read_code(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def read(path: str):
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(path)
    if file_path.is_dir():
        raise IsADirectoryError(path)

    file_type = classify_file(path)
    if file_type == "text":
        content = read_text(path)
    elif file_type == "code":
        content = read_code(path)
    else:
        raise UnsupportedFileTypeError(path)

    return {
        "path": path,
        "type": file_type,
        "content": content,
    }
