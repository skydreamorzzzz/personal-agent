from agent.input import format_input
from agent.planning import planning
from agent.react import react
from llm.client import call_llm
from tools.executor import execute_tool
from tools.schema import LIST_DIRECTORY_TOOL, READ_TOOL


def process_input(user_input: str):
    formatted = format_input(user_input)
    planned = planning(formatted)
    return react(
        planned_input=planned,
        call_llm=call_llm,
        execute_tool=execute_tool,
        tools=[READ_TOOL, LIST_DIRECTORY_TOOL],
    )


if __name__ == "__main__":
    user_input = input("You: ")
    result = process_input(user_input)
    print(result)
