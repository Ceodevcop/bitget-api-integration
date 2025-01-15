from flask import Flask, jsonify, render_template_string
import hashlib
import hmac
import time
import json
import http.client

app = Flask(__name__)

# Bitget API interaction
class BitgetAPI:
    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.base_url = "api.bitget.com"
        self.conn = http.client.HTTPSConnection(self.base_url)

    def _get_headers(self, method, endpoint, params=None):
        timestamp = str(int(time.time() * 1000))  # Current timestamp in ms
        body = json.dumps(params) if params else ""
        prehash_string = timestamp + method + endpoint + body
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            prehash_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "X-BG-API-APIKEY": self.api_key,
            "X-BG-API-PASSPHRASE": self.passphrase,
            "X-BG-API-TIMESTAMP": timestamp,
            "X-BG-API-SIGN": signature
        }

        return headers

    def get_balance(self):
        endpoint = "/api/v1/account/assets"
        method = "GET"
        params = None
        headers = self._get_headers(method, endpoint, params)
        self.conn.request(method, endpoint, body=None, headers=headers)
        response = self.conn.getresponse()
        data = response.read()
        return json.loads(data)

    def get_ticker(self, symbol="BTCUSDT"):
        endpoint = f"/api/v1/market/ticker?symbol={symbol}"
        method = "GET"
        params = None
        self.conn.request(method, endpoint, body=None, headers=None)
        response = self.conn.getresponse()
        data = response.read()
        return json.loads(data)

# HTML and JS for the frontend (embedded in the backend)
@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bitget EA90</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            button { margin: 10px 0; padding: 10px 15px; background-color: #4CAF50; color: white; border: none; }
            button:hover { background-color: #45a049; }
            #output { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>EA90</h1>

        <button onclick="fetchBalance()">Fetch Balance</button>
        <button onclick="fetchTicker()">Get Ticker (BTC/USDT)</button>

        <div id="output">
            <!-- Results will be shown here -->
        </div>

        <script>
            async function fetchBalance() {
                const response = await fetch('/get_balance');
                const data = await response.json();
                document.getElementById('output').innerHTML = "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
            }

            async function fetchTicker() {
                const response = await fetch('/get_ticker');
                const data = await response.json();
                document.getElementById('output').innerHTML = "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
            }
        </script>
    </body>
    </html>
    """)

@app.route('/get_balance')
def get_balance():
    api = BitgetAPI('bg_ffcbb26a743c6f3617a03e4edb87aa3f', 'e397e3420dbb6a1b48dfef734e6ef8d6aaf29ee44a044d51dd1742a8143c0693', '02703242')
    balance = api.get_balance()
    return jsonify(balance)

@app.route('/get_ticker')
def get_ticker():your_api_secret
    api = BitgetAPI('bg_ffcbb26a743c6f3617a03e4edb87aa3f', 'e397e3420dbb6a1b48dfef734e6ef8d6aaf29ee44a044d51dd1742a8143c0693', '02703242
    ticker = api.get_ticker()
    return jsonify(ticker)

if __name__ == '__main__':
    app.run(debug=True)
    
