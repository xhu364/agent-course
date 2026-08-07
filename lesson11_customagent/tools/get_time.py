from langchain_core.tools import tool
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
