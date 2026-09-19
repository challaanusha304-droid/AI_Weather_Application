import os

from groq import Groq


def answer_weather_question(question: str, weather: dict) -> str:
    """Use Groq to answer only with the supplied live weather context."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    context = (
        f"Location: {weather['city']}, {weather['country']}\n"
        f"Conditions: {weather['description']}\n"
        f"Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)\n"
        f"Humidity: {weather['humidity']}%\nWind: {weather['wind_speed']} m/s"
    )
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a concise, practical weather assistant. Base answers on the provided weather context; say when it is insufficient."},
            {"role": "user", "content": f"Weather context:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0.4,
        max_tokens=220,
    )
    return response.choices[0].message.content
