from typing import Dict, AnyStr

import requests
from flask import Flask, jsonify, Response

from utils import get_exchange_rate_uri, get_conversion_uri, get_api_key, APILAYER_KEY_FILE, round_monetary_units


def create_app(config: Dict = dict({})) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(config)

    @app.route("/hello")
    def hello() -> Response:
        """Simple example of an API endpoint"""
        return jsonify({"message": "ohai"})

    @app.route("/hello/<string:name>")
    def hello_name(name: str) -> Response:
        """Simple example using an URL parameter"""
        return jsonify({"message": "ohai {}".format(name)})

    @app.route("/exchange-rate/base/<string:base_currency>/exchange/<string:comparison_currency>")
    def exchange_rate(base_currency: AnyStr, comparison_currency: AnyStr) -> Response:
        """Return the exchange rate of two currencies defined by URL params"""
        base = base_currency.upper()
        comparison = comparison_currency.upper()
        exchange_rate_uri = get_exchange_rate_uri(base, comparison)
        response = requests.get(exchange_rate_uri)
        response_json = (response and response.json()) or dict()
        exchange_data = response_json.get("data", {comparison: {"value": "Error"}})
        exchange_value = exchange_data[comparison].get("value", "0.0")
        return jsonify({
            "original_request": {
                "path": "/exchange-rate",
                "base": base,
                "exchange": comparison,
            },
            "exchange": {
                "base": base,
                "currency": comparison,
                "rate": float(exchange_value)
            }
        })

    @app.route("/convert/base/<string:base_currency>/exchange/<string:comparison_currency>/amount/<string:amount>")
    def exchange_conversion(base_currency: AnyStr, comparison_currency: AnyStr,
                            amount: AnyStr) -> Response:
        """Return the exchange conversion value of two currencies defined by URL params"""
        base = base_currency.upper()
        comparison = comparison_currency.upper()
        normalized_amount = round_monetary_units(amount)
        conversion_uri = get_conversion_uri(comparison, base, normalized_amount)
        headers = {
            "apikey": get_api_key(APILAYER_KEY_FILE)
        }
        response = requests.get(conversion_uri, headers=headers, allow_redirects=True)
        response_json = (response and response.json()) or dict()
        value = str(response_json.get("result"))
        return jsonify({
            "original_request": {
                "path": "/convert",
                "base": base,
                "exchange": comparison,
                "amount": normalized_amount
            },
            "converted_value": round_monetary_units(value),
        })
    return app
