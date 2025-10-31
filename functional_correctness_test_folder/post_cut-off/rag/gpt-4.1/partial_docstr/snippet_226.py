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
        'SGD': 'S$',
        'HKD': 'HK$',
        'MXN': 'MX$',
        'IDR': 'Rp',
        'TRY': '₺',
        'PLN': 'zł',
        'THB': '฿',
        'VND': '₫',
        'NGN': '₦',
        'UAH': '₴',
        'ILS': '₪',
        'SEK': 'kr',
        'NOK': 'kr',
        'DKK': 'kr',
        'CZK': 'Kč',
        'HUF': 'Ft',
        'MYR': 'RM',
        'PHP': '₱',
        'NZD': 'NZ$',
        'SAR': '﷼',
        'AED': 'د.إ',
        'CLP': '$',
        'COP': '$',
        'ARS': '$',
        'PEN': 'S/',
        'TWD': 'NT$',
        'SGD': 'S$',
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
        if price is None:
            return "$--"
        try:
            if price >= 1:
                return f"${price:,.2f}"
            elif price > 0:
                return f"${price:,.6f}".rstrip('0').rstrip('.')
            else:
                return "$0.00"
        except Exception:
            return "$--"

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
            return "$--"
        try:
            return f"${price:,.8f}".rstrip('0').rstrip('.')
        except Exception:
            return "$--"

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
            return "--"
        try:
            if abs(quantity) >= 1:
                return f"{quantity:,.2f}".rstrip('0').rstrip('.')
            elif abs(quantity) > 0:
                return f"{quantity:,.6f}".rstrip('0').rstrip('.')
            else:
                return "0"
        except Exception:
            return "--"

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
            return "--%"
        try:
            pct = float(percentage) * 100
            if abs(pct) >= 1:
                return f"{pct:.2f}%"
            else:
                return f"{pct:.4f}%"
        except Exception:
            return "--%"

    @staticmethod
    def format_price_no_symbol(price: Union[float, int, None]) -> str:
        '''
        Format price without currency symbol, preserving precision.
        Args:
            price: Price value to format
        Returns:
            Formatted price string without currency symbol
        '''
        if price is None:
            return "--"
        try:
            if price >= 1:
                return f"{price:,.2f}"
            elif price > 0:
                return f"{price:,.6f}".rstrip('0').rstrip('.')
            else:
                return "0.00"
        except Exception:
            return "--"

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
            return f"{PriceFormatter._currency_symbols.get(currency.upper(), currency.upper())}--"
        symbol = PriceFormatter._currency_symbols.get(
            currency.upper(), currency.upper())
        try:
            if price >= 1:
                return f"{symbol}{price:,.2f}"
            elif price > 0:
                return f"{symbol}{price:,.6f}".rstrip('0').rstrip('.')
            else:
                return f"{symbol}0.00"
        except Exception:
            return f"{symbol}--"
