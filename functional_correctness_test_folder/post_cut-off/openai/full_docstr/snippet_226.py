
from typing import Union


class PriceFormatter:
    '''Utility class for formatting prices and quantities consistently.'''

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        """
        Format price for user display (UI, console output).
        Args:
            price: Price value to format
        Returns:
            Formatted price string with currency symbol
        """
        return PriceFormatter.format_currency(price, currency='USD')

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
            return 'N/A'
        # 4 decimal places for logging
        return f"${price:,.4f}"

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
            return 'N/A'
        # If quantity is an integer, no decimal places
        if isinstance(quantity, int) or quantity.is_integer():
            return f"{int(quantity):,}"
        # Otherwise, show up to 2 decimal places
        return f"{quantity:,.2f}"

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
            return 'N/A'
        return f"{percentage * 100:,.2f}%"

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        """
        Format price without currency symbol, preserving precision.
        Args:
            price: Price value to format
            force_precision: Optional forced decimal places
        Returns:
            Formatted price string without currency symbol
        """
        if price is None:
            return 'N/A'
        # Default to 2 decimal places, but preserve more if needed
        return f"{price:,.2f}"

    @staticmethod
    def format_currency(price: Union[float, int, None], currency: str = 'USD') -> str:
        """
        Format price with currency symbol.
        Args:
            price: Price value to format
            currency: Currency code (USD, EUR, BTC, etc.)
        Returns:
            Formatted price string with currency symbol
        """
        if price is None:
            return 'N/A'

        # Map common currency codes to symbols
        symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'BTC': '₿',
            'ETH': 'Ξ',
            'CNY': '¥',
            'AUD': 'A$',
            'CAD': 'C$',
            'CHF': 'CHF',
            'SEK': 'kr',
            'NZD': 'NZ$',
        }

        symbol = symbols.get(currency.upper(), f"{currency.upper()} ")
        # Use 2 decimal places for display
        return f"{symbol}{price:,.2f}"
