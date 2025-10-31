
from typing import Union


class PriceFormatter:

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        if price is None:
            return "N/A"
        if isinstance(price, int):
            return str(price)
        return "{0:.2f}".format(price)

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        if price is None:
            return "None"
        return str(price)

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        if quantity is None:
            return "N/A"
        if isinstance(quantity, int):
            return str(quantity)
        return "{0:.4f}".format(quantity)

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        if percentage is None:
            return "N/A"
        return "{0:.2%}".format(percentage)

    @staticmethod
    def format_currency(price: Union[float, int, None], currency: str = 'USD') -> str:
        if price is None:
            return "N/A"
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'BTC': '₿',
            'GBP': '£',
            'JPY': '¥'
        }
        symbol = currency_symbols.get(currency, currency)
        return f"{symbol}{price:.2f}"
