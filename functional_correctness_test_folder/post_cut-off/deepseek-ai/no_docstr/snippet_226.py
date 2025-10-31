
from typing import Union


class PriceFormatter:

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        if price is None:
            return "N/A"
        return "${:,.2f}".format(price)

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        if price is None:
            return "None"
        return "{:.4f}".format(price)

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        if quantity is None:
            return "N/A"
        if isinstance(quantity, int) or quantity.is_integer():
            return "{:,.0f}".format(quantity)
        return "{:,.2f}".format(quantity)

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        if percentage is None:
            return "N/A"
        return "{:.2f}%".format(percentage)

    @staticmethod
    def format_currency(price: Union[float, int, None], currency: str = 'USD') -> str:
        if price is None:
            return "N/A"
        if currency == 'USD':
            return "${:,.2f}".format(price)
        elif currency == 'EUR':
            return "€{:,.2f}".format(price)
        elif currency == 'JPY':
            return "¥{:,.0f}".format(price)
        else:
            return "{:,.2f} {}".format(price, currency)
