
from __future__ import annotations

from typing import Union


class PriceFormatter:
    """Utility class for formatting prices and quantities consistently."""

    _CURRENCY_SYMBOLS = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "CNY": "¥",
        "BTC": "₿",
        "ETH": "Ξ",
        "XRP": "✕",
        "LTC": "Ł",
        "DOGE": "Ð",
    }

    @staticmethod
    def _safe_value(value: Union[float, int, None]) -> Union[float, int, None]:
        """Return the value if it is not None, otherwise return None."""
        return value

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        """
        Format price for user display (UI, console output).
        Args:
            price: Price value to format
        Returns:
            Formatted price string with currency symbol
        """
        if price is None:
            return ""
        try:
            return f"${price:,.2f}"
        except (TypeError, ValueError):
            return str(price)

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        """
        Format price for logging (more precision, with currency symbol).
        Args:
            price: Price value to format
        Returns:
            Formatted price string for logging
        """
        if price is None:
            return ""
        try:
            return f"${price:,.6f}"
        except (TypeError, ValueError):
            return str(price)

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        """
        Format quantity for display.
        Args:
            quantity: Quantity value to format
        Returns:
            Formatted quantity string
        """
        if quantity is None:
            return ""
        try:
            return f"{quantity:,.4f}"
        except (TypeError, ValueError):
            return str(quantity)

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        """
        Format percentage for display.
        Args:
            percentage: Percentage value to format (as decimal, e.g., 0.05 for 5%)
        Returns:
            Formatted percentage string
        """
        if percentage is None:
            return ""
        try:
            return f"{percentage * 100:,.2f}%"
        except (TypeError, ValueError):
            return str(percentage)

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        """
        Format price without currency symbol, preserving precision.
        Args:
            price: Price value to format
        Returns:
            Formatted price string without currency symbol
        """
        if price is None:
            return ""
        try:
            return f"{price:,.2f}"
        except (TypeError, ValueError):
            return str(price)

    @staticmethod
    def format_currency(price: Union[float, int, None], currency: str = "USD") -> str:
        """
        Format price with currency symbol.
        Args:
            price: Price value to format
            currency: Currency code (USD, EUR, BTC, etc.)
        Returns:
            Formatted price string with currency symbol
        """
        if price is None:
            return ""
        symbol = PriceFormatter._CURRENCY_SYMBOLS.get(
            currency.upper(), currency.upper() + " ")
        try:
            return f"{symbol}{price:,.2f}"
        except (TypeError, ValueError):
            return f"{symbol}{price}"
