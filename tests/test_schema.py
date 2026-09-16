from tools.schema import LIST_DIRECTORY_TOOL, READ_TOOL


def test_read_tool_schema():
    function = READ_TOOL["function"]
    parameters = function["parameters"]

    assert function["name"] == "read"
    assert list(parameters["properties"]) == ["path"]
    assert parameters["properties"]["path"]["type"] == "string"
    assert parameters["required"] == ["path"]


def test_list_directory_tool_schema():
    function = LIST_DIRECTORY_TOOL["function"]
    parameters = function["parameters"]

    assert function["name"] == "list_directory"
    assert list(parameters["properties"]) == ["path"]
    assert parameters["properties"]["path"]["type"] == "string"
    assert parameters["required"] == ["path"]
