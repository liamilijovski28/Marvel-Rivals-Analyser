from flask import Flask, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")
API_BASE = "https://marvelrivalsapi.com/api/v1"
HEADERS = { "x-api-key": API_KEY }

@app.route("/api/player/<username>/update")
def update_player(username):
    try:
        print(f"Updating: {username}")
        res = requests.get(f"{API_BASE}/player/{username}/update", headers=HEADERS)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        print("Error in /update:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/player/<username>/match-history")
def player_match_history(username):
    try:
        print(f"Fetching match history for: {username}")
        res = requests.get(f"{API_BASE}/player/{username}/match-history", headers=HEADERS)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        print("Error in /match-history:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/player/<username>/matches")
@app.route("/api/player/<username>/matches")
@app.route("/api/player/<username>/matches")
def player_matches(username):
    try:
        # 1. Try match-history directly
        match_res = requests.get(f"{API_BASE}/player/{username}/match-history", headers=HEADERS)
        match_res.raise_for_status()
        return jsonify(match_res.json())

    except requests.exceptions.HTTPError as http_err:
        # 2. If it failed with 404 or outdated cache, try update (once cooldown expires)
        if http_err.response.status_code == 404:
            return jsonify({"error": "User not found or has no data."}), 404
        else:
            print("[ERROR]", http_err)
            print("Response text:", http_err.response.text)
            return jsonify({
                "error": "HTTP error",
                "detail": http_err.response.text
            }), http_err.response.status_code

    except Exception as e:
        print("[GENERAL ERROR]", e)
        return jsonify({"error": "Unexpected error", "detail": str(e)}), 500
@app.route("/api/player/<username>/profile")
def player_profile(username):
    try:
        res = requests.get(f"{API_BASE}/player/{username}", headers=HEADERS)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        print("Error in /profile:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/heroes")
def get_heroes():
    try:
        res = requests.get(f"{API_BASE}/heroes", headers=HEADERS)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        print("Error in /heroes:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
