from typing import Union, Optional
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


class PriceFormatter:
    '''Utility class for formatting prices and quantities consistently.'''

    @staticmethod
    def _to_decimal(value: Union[float, int, None]) -> Optional[Decimal]:
        if value is None:
            return None
        try:
            # Use str to avoid binary float artifacts where possible
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            return None

    @staticmethod
    def _format_with_grouping(number_str: str) -> str:
        # Splits integer and fractional parts then applies grouping on integer part
        if '.' in number_str:
            int_part, frac_part = number_str.split('.', 1)
        else:
            int_part, frac_part = number_str, ''
        neg = ''
        if int_part.startswith('-'):
            neg = '-'
            int_part = int_part[1:]
        grouped = f"{int(int_part):,}" if int_part else "0"
        if frac_part:
            return f"{neg}{grouped}.{frac_part}"
        return f"{neg}{grouped}"

    @staticmethod
    def _trim_trailing_zeros(num_str: str) -> str:
        if '.' not in num_str:
            return num_str
        num_str = num_str.rstrip('0').rstrip('.')
        return num_str if num_str else '0'

    @staticmethod
    def _quantize(dec: Decimal, decimals: int) -> Decimal:
        if decimals < 0:
            decimals = 0
        quant = Decimal('1').scaleb(-decimals)  # 10^-decimals
        return dec.quantize(quant, rounding=ROUND_HALF_UP)

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
        dec = PriceFormatter._to_decimal(price)
        if dec is None:
            return '-'

        abs_dec = abs(dec)
        # Dynamic precision based on magnitude
        if abs_dec >= Decimal('1'):
            decimals = 2
        elif abs_dec >= Decimal('0.01'):
            decimals = 4
        else:
            decimals = 6

        q = PriceFormatter._quantize(dec, decimals)
        s = f"{q:f}"
        s = PriceFormatter._trim_trailing_zeros(s)
        return PriceFormatter._format_with_grouping(s)

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        '''
        Format price for logging (more precision, with currency symbol).
        Args:
            price: Price value to format
        Returns:
            Formatted price string for logging
        '''
        dec = PriceFormatter._to_decimal(price)
        if dec is None:
            return '-'
        q = PriceFormatter._quantize(dec, 8)
        # Fixed 8 decimals for logs
        s = f"{q:.8f}"
        s = PriceFormatter._format_with_grouping(s)
        return f"${s}"

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        '''
        Format quantity for display.
        Args:
            quantity: Quantity value to format
        Returns:
            Formatted quantity string
        '''
        dec = PriceFormatter._to_decimal(quantity)
        if dec is None:
            return '-'
        # If whole number, no decimals
        if dec == dec.to_integral():
            s = f"{int(dec)}"
            return PriceFormatter._format_with_grouping(s)
        # Up to 6 decimals, trimmed
        q = PriceFormatter._quantize(dec, 6)
        s = f"{q:f}"
        s = PriceFormatter._trim_trailing_zeros(s)
        return PriceFormatter._format_with_grouping(s)

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        '''
        Format percentage for display.
        Args:
            percentage: Percentage value to format (as decimal, e.g., 0.05 for 5%)
        Returns:
            Formatted percentage string
        '''
        dec = PriceFormatter._to_decimal(percentage)
        if dec is None:
            return '-'
        pct = dec * Decimal('100')
        # Up to 2 decimals, trimmed
        q = PriceFormatter._quantize(pct, 2)
        s = f"{q:f}"
        s = PriceFormatter._trim_trailing_zeros(s)
        return f"{s}%"

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
        dec = PriceFormatter._to_decimal(price)
        if dec is None:
            return '-'

        # Use display number formatting without symbol
        num_str = PriceFormatter.format_price_for_display(dec)

        symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CNY': '¥',
            'INR': '₹',
            'KRW': '₩',
            'RUB': '₽',
            'CAD': 'C$',
            'AUD': 'A$',
            'NZD': 'NZ$',
            'CHF': 'CHF ',
            'SEK': 'kr ',
            'NOK': 'kr ',
            'DKK': 'kr ',
            'BTC': '₿',
            'ETH': 'Ξ',
            'USDT': '₮',
            'USDC': '₮',
        }

        code = (currency or '').upper()
        symbol = symbols.get(code)

        if symbol:
            # If symbol already includes trailing space (for some), avoid double space
            joiner = '' if symbol.endswith(' ') else ''
            return f"{symbol}{joiner}{num_str}"
        else:
            return f"{num_str} {code}" if code else num_str
