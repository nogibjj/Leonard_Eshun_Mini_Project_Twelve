from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)


# Load variables from .env
load_dotenv()

# Replace with your API key and endpoint
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "https://open.er-api.com/v6/latest/"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert_currency():
    try:
        data = request.json
        base_currency = data["base_currency"]
        target_currency = data["target_currency"]
        amount = float(data["amount"])

        # Fetch exchange rates
        response = requests.get(f"{BASE_URL}{base_currency}")
        if response.status_code != 200:
            return jsonify({"error": "Unable to fetch exchange rates"}), 500

        rates = response.json().get("rates")
        if target_currency not in rates:
            return jsonify({"error": f"Currency {target_currency} not available"}), 400

        # Calculate converted amount
        rate = rates[target_currency]
        converted_amount = amount * rate

        return jsonify(
            {
                "base_currency": base_currency,
                "target_currency": target_currency,
                "amount": amount,
                "converted_amount": converted_amount,
                "rate": rate,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
