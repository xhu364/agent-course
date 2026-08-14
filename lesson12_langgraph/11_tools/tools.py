from langchain_core.tools import tool


@tool
def calculator(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b