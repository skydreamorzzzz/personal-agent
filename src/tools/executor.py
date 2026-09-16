from tools.list_directory import list_directory
from tools.read import read


def execute_tool(tool_name, arguments):
    if tool_name == "read":
        return read(arguments["path"])
    if tool_name == "list_directory":
        return list_directory(arguments["path"])

    raise ValueError(f"Unknown tool: {tool_name}")
