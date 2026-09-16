import json
from pathlib import Path


def list_directory(path: str) -> str:
    directory = Path(path)

    if not directory.exists():
        raise FileNotFoundError(path)
    if not directory.is_dir():
        raise NotADirectoryError(path)

    entries = []
    for child in sorted(directory.iterdir(), key=lambda item: str(item)):
        if child.is_file():
            entry_type = "file"
        elif child.is_dir():
            entry_type = "directory"
        else:
            continue
        entries.append({"path": str(child), "type": entry_type})

    return json.dumps(
        {"path": path, "entries": entries},
        ensure_ascii=False,
    )
