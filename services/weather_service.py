import os

import requests


WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict:
    """Fetch current weather data from OpenWeather."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY is not configured.")

    try:
        response = requests.get(
            WEATHER_URL,
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=10,
        )
        response.raise_for_status()
    except requests.HTTPError as error:
        if error.response is not None and error.response.status_code == 404:
            raise ValueError(f"I could not find weather for '{city}'.") from error
        raise RuntimeError("Weather data is temporarily unavailable.") from error
    except requests.RequestException as error:
        raise RuntimeError("Weather data is temporarily unavailable.") from error

    data = response.json()
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"].title(),
        "icon": data["weather"][0]["icon"],
    }
