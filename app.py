from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

from services.groq_service import answer_weather_question
from services.weather_service import get_weather

load_dotenv()
app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/weather")
def weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Please provide a city."}), 400
    try:
        return jsonify(get_weather(city))
    except ValueError as error:
        return jsonify({"error": str(error)}), 404
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 503


@app.post("/api/ask")
def ask():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    city = str(data.get("city", "")).strip()
    if not question or not city:
        return jsonify({"error": "A city and question are required."}), 400
    try:
        forecast = get_weather(city)
        return jsonify({"answer": answer_weather_question(question, forecast)})
    except (ValueError, RuntimeError) as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True)
