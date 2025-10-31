
from typing import Union


class PriceFormatter:
    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        """
        Format a price for user‑facing display.
        Uses comma separators and two decimal places.
        """
        if price is None:
            return ""
        try:
            return f"{price:,.2f}"
        except (TypeError, ValueError):
            return ""

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        """
        Format a price for logging purposes.
        Uses four decimal places without comma separators.
        """
        if price is None:
            return ""
        try:
            return f"{price:.4f}"
        except (TypeError, ValueError):
            return ""

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        """
        Format a quantity value.
        If the quantity is effectively an integer, display it without decimals.
        Otherwise, display two decimal places.
        """
        if quantity is None:
            return ""
        try:
            if isinstance(quantity, (int, float)):
                if abs(quantity - round(quantity)) < 1e-6:
                    return str(int(round(quantity)))
                else:
                    return f"{quantity:.2f}"
            return str(quantity)
        except (TypeError, ValueError):
            return ""

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        """
        Format a percentage value with two decimal places followed by a percent sign.
        """
        if percentage is None:
            return ""
        try:
            return f"{percentage:.2f}%"
        except (TypeError, ValueError):
            return ""

    # Duplicate method – kept for backward compatibility
    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        """
        Duplicate of the first format_price_for_display method.
        """
        return PriceFormatter.format_price_for_display(price)

    @staticmethod
    def format_currency(price: Union[float, int, None], currency: str = 'USD') -> str:
        """
        Format a price with a currency code.
        Uses comma separators and two decimal places.
        """
        if price is None:
            return currency
        try:
            return f"{currency} {price:,.2f}"
        except (TypeError, ValueError):
            return currency
