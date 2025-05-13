import requests
import json
import os
from flask import Flask, request

app = Flask(__name__)

API_KEY = os.getenv("DELTA_API_KEY")
API_SECRET = os.getenv("DELTA_API_SECRET")

symbol_to_product_id = {
    "SOLUSD.P": 1326,
    "BTCUSD.P": 105,
    "ETHUSD.P": 110
}

def place_order(symbol, side, qty):
    product_id = symbol_to_product_id.get(symbol)
    if not product_id:
        return {"error": f"Unknown symbol: {symbol}"}

    url = "https://api.delta.exchange/orders"

    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "product_id": product_id,
        "size": float(qty),
        "side": side.upper(),
        "order_type": "market",
        "time_in_force": "gtc"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

@app.route("/", methods=["GET"])
def home():
    return "Delta Auto Trader Running ✅"

@app.route("/myip", methods=["GET"])
def get_my_ip():
    return request.headers.get("X-Forwarded-For", request.remote_addr)

@app.route("/alert", methods=["POST"])
def handle_alert():
    try:
        alert_data = request.json
        symbol = alert_data["symbol"]
        side = alert_data["side"]
        qty = alert_data["qty"]

        result = place_order(symbol, side, qty)
        return {"status": "executed", "result": result}

    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
