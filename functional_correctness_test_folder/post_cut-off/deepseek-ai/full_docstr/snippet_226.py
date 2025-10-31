
from typing import Union


class PriceFormatter:
    '''Utility class for formatting prices and quantities consistently.'''
    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        '''
        Format price for user display (UI, console output).
        Args:
            price: Price value to format
        Returns:
            Formatted price string with currency symbol
        '''
        if price is None:
            return "N/A"
        return f"${price:,.2f}"

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        '''
        Format price for logging (more precision, with currency symbol).
        Args:
            price: Price value to format
        Returns:
            Formatted price string for logging
        '''
        if price is None:
            return "N/A"
        return f"${price:.6f}"

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        '''
        Format quantity for display.
        Args:
            quantity: Quantity value to format
        Returns:
            Formatted quantity string
        '''
        if quantity is None:
            return "N/A"
        if isinstance(quantity, int) or quantity.is_integer():
            return f"{int(quantity):,}"
        return f"{quantity:,.2f}"

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        '''
        Format percentage for display.
        Args:
            percentage: Percentage value to format (as decimal, e.g., 0.05 for 5%)
        Returns:
            Formatted percentage string
        '''
        if percentage is None:
            return "N/A"
        return f"{percentage * 100:.2f}%"

    @staticmethod
    def format_price_without_currency(price: Union[float, int, None], force_precision: int = None) -> str:
        '''
        Format price without currency symbol, preserving precision.
        Args:
            price: Price value to format
            force_precision: Optional forced decimal places
        Returns:
            Formatted price string without currency symbol
        '''
        if price is None:
            return "N/A"
        if force_precision is not None:
            return f"{price:,.{force_precision}f}"
        if isinstance(price, int) or price.is_integer():
            return f"{int(price):,}"
        return f"{price:,.2f}"

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
        if price is None:
            return "N/A"
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'BTC': '₿',
        }
        symbol = currency_symbols.get(currency, currency)
        return f"{symbol}{price:,.2f}"
