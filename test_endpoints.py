import json
from typing import Dict

import pytest

from utils import Currencies


class MockedResponse:
    def __init__(self, deserialized_json: Dict, status_code: int):
        self.deserialized_json = deserialized_json
        self.status_code = status_code

    def json(self):
        return self.deserialized_json


def test_hello(test_client):
    response = test_client.get("/hello")
    assert json.loads(response.data) == {"message": "ohai"}


def test_hello_name(test_client):
    response = test_client.get("/hello/kalliope")
    assert json.loads(response.data) == {"message": "ohai kalliope"}


@pytest.mark.parametrize("test_data", [
    (Currencies.USD, 0.123),
    (Currencies.GBP, 0.23445),
    (Currencies.EUR, 0.654342)
])
def test_exchange_rate(test_client, mocker, test_data):
    mock_get = mocker.patch("app.requests.get")
    comparison = test_data[0]
    exchange_value = test_data[1]
    mock_get.return_value = MockedResponse({"data": {comparison: {"value": exchange_value}}}, 200)
    response = test_client.get(f"/exchange-rate/base/usd/exchange/{comparison}")
    assert json.loads(response.data) == {
            "original_request": {
                "path": "/exchange-rate",
                "base": "USD",
                "exchange": comparison,
            },
            "exchange": {
                "base": "USD",
                "currency": comparison,
                "rate": exchange_value
            }
        }


def test_conversion(test_client, mocker):
    mock_get = mocker.patch("app.requests.get")
    comparison = "GBP"
    exchange_value = "10.00"
    mock_get.return_value = MockedResponse({
        "success": True,
        "query": {
            "from": "GBP",
            "to": "USD",
            "amount": 10
        },
        "info": {
            "timestamp": 1667887743,
            "quote": 1.149339
        },
        "result": 11.49339
    }, 200)
    response = test_client.get(f"/convert/base/usd/exchange/gbp/amount/{exchange_value}")
    assert json.loads(response.data) == {
            "original_request": {
                "path": "/convert",
                "base": "USD",
                "exchange": comparison,
                "amount": exchange_value,
            },
            "converted_value": "11.49"
        }
