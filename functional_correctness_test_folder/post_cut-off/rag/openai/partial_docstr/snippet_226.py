
from __future__ import annotations

from typing import Union


class PriceFormatter:
    '''Utility class for formatting prices and quantities consistently.'''

    _CURRENCY_SYMBOLS = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'CNY': '¥',
        'BTC': '₿',
        'ETH': 'Ξ',
        'XRP': '✕',
        'LTC': 'Ł',
    }

    @staticmethod
    def _safe_float(value: Union[float, int, None]) -> Union[float, None]:
        """Return a float or None if the value is None or not numeric."""
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        '''
        Format price for user display (UI, console output).
        Args:
            price: Price value to format
        Returns:
            Formatted price string with currency symbol
        '''
        f = PriceFormatter._safe_float(price)
        if f is None:
            return ''
        return f"${f:,.2f}"

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        '''
        Format price for logging (more precision, with currency symbol).
        Args:
            price: Price value to format
        Returns:
            Formatted price string for logging
        '''
        f = PriceFormatter._safe_float(price)
        if f is None:
            return ''
        return f"${f:,.6f}"

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        '''
        Format quantity for display.
        Args:
            quantity: Quantity value to format
        Returns:
            Formatted quantity string
        '''
        f = PriceFormatter._safe_float(quantity)
        if f is None:
            return ''
        # Use up to 4 decimal places, strip trailing zeros
        return f"{f:,.4f}".rstrip('0').rstrip('.')

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        '''
        Format percentage for display.
        Args:
            percentage: Percentage value to format (as decimal, e.g., 0.05 for 5%)
        Returns:
            Formatted percentage string
        '''
        f = PriceFormatter._safe_float(percentage)
        if f is None:
            return ''
        return f"{f * 100:.2f}%"

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        '''
        Format price without currency symbol, preserving precision.
        Args:
            price: Price value to format
            force_precision: Optional forced decimal places
        Returns:
            Formatted price string without currency symbol
        '''
        f = PriceFormatter._safe_float(price)
        if f is None:
            return ''
        # Preserve up to 6 decimal places, strip trailing zeros
        return f"{f:,.6f}".rstrip('0').rstrip('.')

    @staticmethod
    def format_currency(price: Union[float, int, None], currency: str = 'USD') -> str:
        '''
        Format price with currency symbol.
        Args:
            price: Price value to format
            currency: Currency code (USD, EUR, BTC, etc.)
        Returns:
            Formatted price string with currency symbol
        '''
        f = PriceFormatter._safe_float(price)
        if f is None:
            return ''
        symbol = PriceFormatter._CURRENCY_SYMBOLS.get(
            currency.upper(), currency.upper() + ' ')
        return f"{symbol}{f:,.2f}"
