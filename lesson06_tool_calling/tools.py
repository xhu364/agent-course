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


def calculator(number1, number2):
    """
    Sum of two numbers

    Args:
        number1: the 1st number
        number2: the 2nd number

    Returns:
        summation of two input numbers
    """

    return number1 + number2
