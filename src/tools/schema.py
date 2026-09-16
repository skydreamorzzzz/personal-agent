READ_TOOL = {
    "type": "function",
    "function": {
        "name": "read",
        "description": (
            "读取本地文件内容。第一版只支持纯文本和源代码文件，支持 "
            "txt、md、log、json、yaml、yml、py、c、cpp、h、hpp、java、js、ts。"
            "暂不支持 PDF、Word/DOCX、Excel/XLSX、图片、二进制文件或 URL。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "要读取的本地文件路径",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
}

LIST_DIRECTORY_TOOL = {
    "type": "function",
    "function": {
        "name": "list_directory",
        "description": (
            "List the direct children of a local directory. Returns files and "
            "subdirectories as structured JSON. This tool is non-recursive."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "要列出的本地目录路径",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
}
