from typing import Union


class PriceFormatter:
    '''Utility class for formatting prices and quantities consistently.'''

    _currency_symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'BTC': '₿',
        'ETH': 'Ξ',
        'CNY': '¥',
        'INR': '₹',
        'RUB': '₽',
        'KRW': '₩',
        'AUD': 'A$',
        'CAD': 'C$',
        'CHF': 'Fr.',
        'BRL': 'R$',
        'ZAR': 'R',
        'TRY': '₺',
        'MXN': '$',
        'SGD': 'S$',
        'HKD': 'HK$',
        'NZD': 'NZ$',
        'PLN': 'zł',
        'SEK': 'kr',
        'NOK': 'kr',
        'DKK': 'kr',
        'THB': '฿',
        'IDR': 'Rp',
        'PHP': '₱',
        'MYR': 'RM',
        'VND': '₫',
        'ILS': '₪',
        'SAR': '﷼',
        'AED': 'د.إ',
        'COP': '$',
        'CLP': '$',
        'PEN': 'S/',
        'ARS': '$',
        'CZK': 'Kč',
        'HUF': 'Ft',
        'RON': 'lei',
        'BGN': 'лв',
        'HRK': 'kn',
        'UAH': '₴',
        'BTC': '₿',
        'ETH': 'Ξ',
        'USDT': '₮',
        'USDC': '₮',
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
        return PriceFormatter.format_currency(price, currency='USD')

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
            return '$--'
        try:
            return f"${price:,.8f}"
        except Exception:
            return '$--'

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
            return '--'
        try:
            if abs(quantity) >= 1:
                return f"{quantity:,.2f}"
            elif abs(quantity) > 0:
                return f"{quantity:.6f}".rstrip('0').rstrip('.')
            else:
                return "0"
        except Exception:
            return '--'

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
            return '--%'
        try:
            return f"{percentage * 100:.2f}%"
        except Exception:
            return '--%'

    @staticmethod
    def format_price_without_symbol(price: Union[float, int, None]) -> str:
        '''
        Format price without currency symbol, preserving precision.
        Args:
            price: Price value to format
        Returns:
            Formatted price string without currency symbol
        '''
        if price is None:
            return '--'
        try:
            if abs(price) >= 1:
                return f"{price:,.2f}"
            elif abs(price) > 0:
                return f"{price:.8f}".rstrip('0').rstrip('.')
            else:
                return "0"
        except Exception:
            return '--'

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
        symbol = PriceFormatter._currency_symbols.get(
            currency.upper(), currency.upper() + ' ')
        if price is None:
            return f"{symbol}--"
        try:
            if abs(price) >= 1:
                formatted = f"{price:,.2f}"
            elif abs(price) > 0:
                formatted = f"{price:.8f}".rstrip('0').rstrip('.')
            else:
                formatted = "0"
            if symbol in {'$', '€', '£', '¥', '₿', 'Ξ', '₮', '₽', '₩', '₹', '₺', '฿', '₱', '₫', '₪', '﷼', '₴', 'zł', 'Ft', 'Kč', 'Fr.', 'R$', 'S/', 'lei', 'лв', 'kn'}:
                return f"{symbol}{formatted}"
            else:
                return f"{formatted} {symbol}".strip()
        except Exception:
            return f"{symbol}--"
