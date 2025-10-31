
from typing import Union


class PriceFormatter:
    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        '''
        Format price without currency symbol, preserving precision.
        Args:
            price: Price value to format
        Returns:
            Formatted price string without currency symbol
        '''
        if price is None:
            return "-"
        if isinstance(price, int):
            return f"{price:,}"
        # For floats, preserve up to 8 decimals, but trim trailing zeros
        formatted = f"{price:,.8f}".rstrip('0').rstrip('.')
        return formatted

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        if price is None:
            return "None"
        if isinstance(price, int):
            return str(price)
        return f"{price:.8f}"

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        if quantity is None:
            return "-"
        if isinstance(quantity, int):
            return f"{quantity:,}"
        formatted = f"{quantity:,.8f}".rstrip('0').rstrip('.')
        return formatted

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
            return "-"
        value = percentage * 100
        if abs(value) >= 1:
            formatted = f"{value:,.2f}".rstrip('0').rstrip('.')
        else:
            formatted = f"{value:.4f}".rstrip('0').rstrip('.')
        return f"{formatted}%"

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
            return "-"
        symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'BTC': '₿',
            'ETH': 'Ξ',
            'CNY': '¥',
            'INR': '₹',
        }
        symbol = symbols.get(currency.upper(), currency.upper() + " ")
        formatted = PriceFormatter.format_price_for_display(price)
        if symbol in {'₿', 'Ξ'}:
            return f"{symbol}{formatted}"
        elif symbol in {'$', '€', '£', '¥', '₹'}:
            return f"{symbol}{formatted}"
        else:
            return f"{symbol}{formatted}"
