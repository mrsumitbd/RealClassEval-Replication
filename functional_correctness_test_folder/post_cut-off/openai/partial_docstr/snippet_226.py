
from typing import Union
from decimal import Decimal, ROUND_HALF_UP


class PriceFormatter:
    _CURRENCY_SYMBOLS = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'AUD': 'A$',
        'CAD': 'C$',
        'BTC': '₿',
        'ETH': 'Ξ',
        'LTC': 'Ł',
        'XRP': '✕',
    }

    @staticmethod
    def _to_decimal(value: Union[float, int, None]) -> Decimal:
        if value is None:
            return None
        return Decimal(str(value))

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        """
        Format price without currency symbol, preserving precision.
        """
        if price is None:
            return "N/A"
        d = PriceFormatter._to_decimal(price)
        # Normalize to remove trailing zeros
        s = format(d.normalize(), 'f')
        # Remove trailing decimal point if integer
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        return s

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        """
        Format price for logging: include currency symbol and two decimal places.
        """
        return PriceFormatter.format_currency(price, currency='USD')

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        """
        Format quantity with up to 8 decimal places, stripping trailing zeros.
        """
        if quantity is None:
            return "N/A"
        d = PriceFormatter._to_decimal(quantity)
        # Quantize to 8 decimal places
        d = d.quantize(Decimal('0.00000001'), rounding=ROUND_HALF_UP)
        s = format(d.normalize(), 'f')
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        return s

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
            return "N/A"
        d = PriceFormatter._to_decimal(percentage) * Decimal('100')
        d = d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"{d}%"

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
            return "N/A"
        symbol = PriceFormatter._CURRENCY_SYMBOLS.get(currency.upper(), '')
        d = PriceFormatter._to_decimal(price)
        d = d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"{symbol}{d}"
