from langchain_core.tools import tool


@tool
def get_weather(city):
    """
    Get weather information.

    Args:
        city: city name

    Returns:
        weather information
    """

    weather = {
        "Boston": "Sunny, 80F",
        "Seattle": "Rainy, 55F",
        "New York": "Cloudy, 70F",
    }

    return weather.get(city, "Unknown city")
