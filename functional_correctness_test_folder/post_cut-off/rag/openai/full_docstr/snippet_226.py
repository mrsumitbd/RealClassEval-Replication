
from __future__ import annotations

from typing import Union


class PriceFormatter:
    '''Utility class for formatting prices and quantities consistently.'''

    _currency_symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'CNY': '¥',
        'KRW': '₩',
        'BTC': '₿',
        'ETH': 'Ξ',
        'AUD': 'A$',
        'CAD': 'C$',
        'CHF': 'CHF',
        'NZD': 'NZ$',
    }

    @staticmethod
    def _safe_number(value: Union[float, int, None]) -> Union[float, int, None]:
        """Return the value if it is a number, otherwise None."""
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
        num = PriceFormatter._safe_number(price)
        if num is None:
            return ''
        # Default to USD
        symbol = PriceFormatter._currency_symbols.get('USD', '$')
        return f'{symbol}{num:,.2f}'

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        '''
        Format price for logging (more precision, with currency symbol).
        Args:
            price: Price value to format
        Returns:
            Formatted price string for logging
        '''
        num = PriceFormatter._safe_number(price)
        if num is None:
            return ''
        # Default to USD
        symbol = PriceFormatter._currency_symbols.get('USD', '$')
        # 8 decimal places for logging
        return f'{symbol}{num:,.8f}'

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        '''
        Format quantity for display.
        Args:
            quantity: Quantity value to format
        Returns:
            Formatted quantity string
        '''
        num = PriceFormatter._safe_number(quantity)
        if num is None:
            return ''
        # 4 decimal places for quantity
        return f'{num:,.4f}'

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        '''
        Format percentage for display.
        Args:
            percentage: Percentage value to format (as decimal, e.g., 0.05 for 5%)
        Returns:
            Formatted percentage string
        '''
        num = PriceFormatter._safe_number(percentage)
        if num is None:
            return ''
        return f'{num * 100:,.2f}%'

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        '''
        Format price without currency symbol, preserving precision.
        Args:
            price: Price value to format
        Returns:
            Formatted price string without currency symbol
        '''
        num = PriceFormatter._safe_number(price)
        if num is None:
            return ''
        # Preserve up to 8 decimal places, strip trailing zeros
        formatted = f'{num:.8f}'.rstrip('0').rstrip('.')
        return formatted

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
        num = PriceFormatter._safe_number(price)
        if num is None:
            return ''
        symbol = PriceFormatter._currency_symbols.get(
            currency.upper(), currency + ' ')
        return f'{symbol}{num:,.2f}'
