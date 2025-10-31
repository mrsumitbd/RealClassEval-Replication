
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
        'INR': '₹',
        'RUB': '₽',
        'KRW': '₩',
        'AUD': 'A$',
        'CAD': 'C$',
        'CHF': 'Fr.',
        'SGD': 'S$',
        'HKD': 'HK$',
        'BRL': 'R$',
        'ZAR': 'R',
        'TRY': '₺',
        'MXN': '$',
        'IDR': 'Rp',
        'THB': '฿',
        'PLN': 'zł',
        'SEK': 'kr',
        'NOK': 'kr',
        'DKK': 'kr',
        'CZK': 'Kč',
        'HUF': 'Ft',
        'ILS': '₪',
        'MYR': 'RM',
        'PHP': '₱',
        'TWD': 'NT$',
        'VND': '₫',
        'SAR': '﷼',
        'AED': 'د.إ',
        'NZD': 'NZ$',
        'XAU': 'Au',
        'XAG': 'Ag',
    }

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        '''
        Format price for user display (UI, console output).
        Args:
            price: Price value to format
        Returns:
            Formatted price string with currency symbol
        '''
        return PriceFormatter.format_currency(price, 'USD')

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
            return '$0.00000000'
        try:
            return f"${float(price):,.8f}"
        except Exception:
            return '$0.00000000'

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
            return '0'
        try:
            q = float(quantity)
            if q == int(q):
                return f"{int(q)}"
            elif abs(q) >= 1:
                return f"{q:,.4f}".rstrip('0').rstrip('.')
            else:
                return f"{q:.8f}".rstrip('0').rstrip('.')
        except Exception:
            return '0'

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
            return '0%'
        try:
            pct = float(percentage) * 100
            if abs(pct) >= 1:
                return f"{pct:.2f}%".rstrip('0').rstrip('.')
            else:
                return f"{pct:.4f}%".rstrip('0').rstrip('.')
        except Exception:
            return '0%'

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
            return '0'
        try:
            p = float(price)
            if force_precision is not None:
                fmt = f"{{:,.{force_precision}f}}"
                return fmt.format(p)
            if abs(p) >= 1:
                s = f"{p:,.2f}"
                if '.' in s:
                    s = s.rstrip('0').rstrip('.')
                return s
            else:
                s = f"{p:.8f}"
                s = s.rstrip('0').rstrip('.')
                return s
        except Exception:
            return '0'

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
            price = 0
        symbol = PriceFormatter._CURRENCY_SYMBOLS.get(
            currency.upper(), currency.upper() + ' ')
        try:
            p = float(price)
            if abs(p) >= 1:
                s = f"{p:,.2f}"
                if '.' in s:
                    s = s.rstrip('0').rstrip('.')
            else:
                s = f"{p:.8f}".rstrip('0').rstrip('.')
            if symbol in {'₿', 'Ξ', 'Au', 'Ag'}:
                return f"{s} {symbol}"
            elif symbol.endswith(' '):
                return f"{symbol}{s}"
            else:
                return f"{symbol}{s}"
        except Exception:
            return f"{symbol}0"
