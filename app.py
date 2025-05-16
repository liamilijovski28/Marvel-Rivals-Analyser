from fetch import create_app, db
from fetch.config import DevelopmentConfig
from flask_migrate import Migrate
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
from flask import jsonify


load_dotenv()

app = create_app(DevelopmentConfig) 
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)


API_KEY = os.getenv("API_KEY")
API_BASE = "https://marvelrivalsapi.com/api/v1"
HEADERS = {"x-api-key": API_KEY}


@app.route("/api/player/<username>/update")
def update_player(username):
    try:
        res = requests.get(f"{API_BASE}/player/{username}/update", headers=HEADERS)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/player/<username>/match-history")
def player_match_history(username):
    try:
        res = requests.get(f"{API_BASE}/player/{username}/match-history", headers=HEADERS)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/player/<username>/matches")
def player_matches(username):
    try:
        res = requests.get(f"{API_BASE}/player/{username}/match-history", headers=HEADERS)
        res.raise_for_status()
        return jsonify(res.json())
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 404:
            return jsonify({"error": "User not found or has no data."}), 404
        return jsonify({"error": "HTTP error", "detail": http_err.response.text}), http_err.response.status_code
    except Exception as e:
        return jsonify({"error": "Unexpected error", "detail": str(e)}), 500


@app.route("/api/player/<username>/profile")
def player_profile(username):
    try:
        res = requests.get(f"{API_BASE}/player/{username}", headers=HEADERS)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/heroes")
def get_heroes():
    try:
        res = requests.get(f"{API_BASE}/heroes", headers=HEADERS)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

