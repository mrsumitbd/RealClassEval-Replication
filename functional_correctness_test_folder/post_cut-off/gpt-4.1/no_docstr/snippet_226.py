
from typing import Union


class PriceFormatter:

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        if price is None:
            return "-"
        if isinstance(price, int):
            return f"${price:,d}"
        return f"${price:,.2f}"

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        if price is None:
            return "None"
        return f"{price:.8f}"

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        if quantity is None:
            return "-"
        if isinstance(quantity, int):
            return f"{quantity:,d}"
        return f"{quantity:,.4f}"

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        if percentage is None:
            return "-"
        return f"{percentage:.2f}%"

    @staticmethod
    def format_currency(price: Union[float, int, None], currency: str = 'USD') -> str:
        if price is None:
            return "-"
        symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CNY': '¥',
            'INR': '₹',
        }
        symbol = symbols.get(currency.upper(), currency.upper() + " ")
        if isinstance(price, int):
            return f"{symbol}{price:,d}"
        return f"{symbol}{price:,.2f}"
