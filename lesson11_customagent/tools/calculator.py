from langchain_core.tools import tool


@tool
def calculator(expression):
    """
    Evaluate the result of a mathematical expression.

    Args:
        expression: A mathematical expression string.
                    Examples:
                    "1000 + 123"
                    "(50 * 20) / 5"

    Returns:
        The calculated result.
    """

    try:
        result = eval(expression)
        return result

    except Exception as e:
        return f"Invalid expression: {e}"
