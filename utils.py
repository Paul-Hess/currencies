from typing import Text, AnyStr, List
from pathlib import Path
from dataclasses import dataclass, fields
from decimal import Decimal, ROUND_HALF_UP

CURRENCY_API_KEY_FILE = ".currency-api-key.txt"
APILAYER_KEY_FILE = ".apilayer-api-key.txt"
CURRENCY_API_BASE_URL = "https://api.currencyapi.com/v3"
APILAYER_API_BASE_URL = "https://api.apilayer.com/currency_data"


@dataclass
class Currencies:
    USD: AnyStr = "USD"
    GBP: AnyStr = "GBP"
    EUR: AnyStr = "EUR"


supported_currencies: List[AnyStr] = [field.name.upper() for field in fields(Currencies)]


def get_api_key(key_file: AnyStr) -> Text:
    api_key_path = Path().home().resolve().joinpath(key_file)
    with api_key_path.open(mode="r", encoding="utf-8") as read_file:
        return read_file.read().strip()


def get_exchange_rate_uri(from_currency: AnyStr, to_currency: AnyStr) -> Text:
    api_key = get_api_key(CURRENCY_API_KEY_FILE)
    return "{url}/latest?apikey={key}&currencies={to_currency}&base_currency={from_currency}".format(
        url=CURRENCY_API_BASE_URL,
        key=api_key,
        to_currency=getattr(Currencies, to_currency),
        from_currency=getattr(Currencies, from_currency),
    )


def get_conversion_uri(from_currency: AnyStr, to_currency: AnyStr, amount: Decimal) -> Text:
    return "{url}/convert?to={to_currency}&from={from_currency}&amount={amount}".format(
        url=APILAYER_API_BASE_URL,
        to_currency=getattr(Currencies, to_currency),
        from_currency=getattr(Currencies, from_currency),
        amount=amount
    )


def round_monetary_units(currency_value: AnyStr) -> Decimal:
    cents = Decimal(".01")
    return Decimal(currency_value).quantize(cents, ROUND_HALF_UP)
