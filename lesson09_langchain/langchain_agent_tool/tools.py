from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Calculate mathematical expressions.

    Args:
        expression:
            math expression like "10 * 5"

    Returns:
        calculation result
    """

    try:
        result = eval(expression)
        return str(result)

    except Exception as e:
        return f"Error: {e}"


@tool
def get_weather(city: str):
    """
    get weather information for a given city

    Args:
        city:
            city for which weather is required
    Returns:
        return weather information
    """
    return f"temperature for {city} is 80F"
