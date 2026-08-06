from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
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


from datetime import datetime
from zoneinfo import ZoneInfo


@tool
def get_time(city):
    """
    Get the current local time for a city.

    Args:
        city: Name of the city.

    Returns:
        Current local date and time as a formatted string,
        or an error message if the city is unknown.
    """

    city_timezones = {
        "Boston": "America/New_York",
        "New York": "America/New_York",
        "Seattle": "America/Los_Angeles",
        "Los Angeles": "America/Los_Angeles",
        "Chicago": "America/Chicago",
        "Denver": "America/Denver",
        "London": "Europe/London",
        "Paris": "Europe/Paris",
        "Berlin": "Europe/Berlin",
        "Tokyo": "Asia/Tokyo",
        "Shanghai": "Asia/Shanghai",
        "Beijing": "Asia/Shanghai",
        "Hong Kong": "Asia/Hong_Kong",
        "Singapore": "Asia/Singapore",
        "Sydney": "Australia/Sydney",
    }

    timezone = city_timezones.get(city)

    if timezone is None:
        return f"Unknown city: {city}"

    current_time = datetime.now(ZoneInfo(timezone))

    return current_time.strftime("%Y-%m-%d %I:%M:%S %p %Z")


def get_wikipedia_tool():
    """
    Returns a LangChain Wikipedia Tool.
    """

    wikipedia = WikipediaAPIWrapper(
        top_k_results=1,
        doc_content_chars_max=1000,
    )

    return WikipediaQueryRun(api_wrapper=wikipedia)


class ToolRegister:
    def __init__(self):
        self.tools = []

    def register(self, tool):
        self.tools.append(tool)

    def get_tools(self):
        return self.tools
