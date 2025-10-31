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
        'PLN': 'zł',
        'SEK': 'kr',
        'NOK': 'kr',
        'DKK': 'kr',
        'NZD': 'NZ$',
        'THB': '฿',
        'IDR': 'Rp',
        'MYR': 'RM',
        'PHP': '₱',
        'VND': '₫',
        'ILS': '₪',
        'SAR': '﷼',
        'AED': 'د.إ',
        'CZK': 'Kč',
        'HUF': 'Ft',
        'CLP': '$',
        'COP': '$',
        'ARS': '$',
        'PEN': 'S/',
        'TWD': 'NT$',
        'SGD': 'S$',
        'KRW': '₩',
        'BTC': '₿',
        'ETH': 'Ξ',
        # Add more as needed
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
            return '--'
        try:
            value = float(price)
        except (TypeError, ValueError):
            return '--'
        if value >= 1:
            formatted = f"${value:,.2f}"
        elif value > 0:
            formatted = f"${value:,.6f}".rstrip('0').rstrip('.')
        else:
            formatted = "$0.00"
        return formatted

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
            return '--'
        try:
            value = float(price)
        except (TypeError, ValueError):
            return '--'
        formatted = f"${value:,.8f}".rstrip('0').rstrip('.')
        return formatted

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
            value = float(quantity)
        except (TypeError, ValueError):
            return '--'
        if value >= 1:
            formatted = f"{value:,.2f}"
        elif value > 0:
            formatted = f"{value:,.6f}".rstrip('0').rstrip('.')
        else:
            formatted = "0.00"
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
            return '--'
        try:
            value = float(percentage) * 100
        except (TypeError, ValueError):
            return '--'
        if abs(value) >= 1:
            formatted = f"{value:.2f}%"
        else:
            formatted = f"{value:.4f}%"
        return formatted

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
        if price is None:
            return '--'
        try:
            value = float(price)
        except (TypeError, ValueError):
            return '--'
        if value >= 1:
            formatted = f"{value:,.2f}"
        elif value > 0:
            formatted = f"{value:,.6f}".rstrip('0').rstrip('.')
        else:
            formatted = "0.00"
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
        if price is None:
            return '--'
        try:
            value = float(price)
        except (TypeError, ValueError):
            return '--'
        symbol = PriceFormatter._currency_symbols.get(
            currency.upper(), currency.upper() + ' ')
        if value >= 1:
            formatted = f"{symbol}{value:,.2f}"
        elif value > 0:
            formatted = f"{symbol}{value:,.6f}".rstrip('0').rstrip('.')
        else:
            formatted = f"{symbol}0.00"
        return formatted
