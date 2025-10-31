from typing import Union
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


class PriceFormatter:
    '''Utility class for formatting prices and quantities consistently.'''

    _CURRENCY_SYMBOLS = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'CNY': '¥',
        'INR': '₹',
        'AUD': 'A$',
        'CAD': 'C$',
        'CHF': 'CHF',
        'KRW': '₩',
        'RUB': '₽',
        'SGD': 'S$',
        'NZD': 'NZ$',
        'ZAR': 'R',
        'BTC': '₿',
        'ETH': 'Ξ',
        'USDT': 'USDT',
    }

    _CURRENCY_DECIMALS = {
        'USD': 2,
        'EUR': 2,
        'GBP': 2,
        'JPY': 0,
        'CNY': 2,
        'INR': 2,
        'AUD': 2,
        'CAD': 2,
        'CHF': 2,
        'KRW': 0,
        'RUB': 2,
        'SGD': 2,
        'NZD': 2,
        'ZAR': 2,
        'BTC': 8,
        'ETH': 6,
        'USDT': 2,
    }

    @staticmethod
    def _to_decimal(value: Union[float, int, Decimal, None]) -> Union[Decimal, None]:
        if value is None:
            return None
        try:
            if isinstance(value, Decimal):
                d = value
            elif isinstance(value, int):
                d = Decimal(value)
            elif isinstance(value, float):
                d = Decimal(str(value))
            else:
                # fallback for strings or other numeric-like inputs
                d = Decimal(value)
            if d.is_nan() or d.is_infinite():
                return None
            return d
        except (InvalidOperation, ValueError, TypeError):
            return None

    @staticmethod
    def _group_number_str(s: str) -> str:
        neg = s.startswith('-')
        if neg:
            s = s[1:]
        if '.' in s:
            int_part, frac_part = s.split('.', 1)
        else:
            int_part, frac_part = s, ''
        try:
            int_grouped = f"{int(int_part):,}"
        except ValueError:
            int_grouped = int_part
        res = int_grouped + ('.' + frac_part if frac_part else '')
        return '-' + res if neg else res

    @staticmethod
    def _format_decimal(
        d: Decimal,
        *,
        max_frac: int,
        min_frac: int = 0,
        grouping: bool = True,
        trim_trailing_zeros: bool = True,
    ) -> str:
        q = Decimal(1).scaleb(-max_frac)  # 10^-max_frac
        dq = d.quantize(q, rounding=ROUND_HALF_UP)
        s = format(dq, 'f')

        if '.' in s:
            int_part, frac = s.split('.', 1)
        else:
            int_part, frac = s, ''

        if trim_trailing_zeros:
            frac = frac.rstrip('0')
            if len(frac) < min_frac:
                frac = frac + '0' * (min_frac - len(frac))
        else:
            if len(frac) < min_frac:
                frac = frac + '0' * (min_frac - len(frac))

        s = int_part + ('.' + frac if frac else '')
        return PriceFormatter._group_number_str(s) if grouping else s

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        '''
        Format price for user display (UI, console output).
        Args:
            price: Price value to format
        Returns:
            Formatted price string with currency symbol
        '''
        # This definition is shadowed by the later one in Python; see the later method.

        # Provide a minimal fallback to avoid accidental usage if import order changes.
        d = PriceFormatter._to_decimal(price)
        if d is None:
            return 'N/A'
        # Default to USD-like formatting with symbol via format_currency
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
        d = PriceFormatter._to_decimal(price)
        if d is None:
            return 'N/A'
        # Use higher precision for logging, default currency USD
        number_str = PriceFormatter._format_decimal(
            d, max_frac=8, min_frac=2, grouping=True, trim_trailing_zeros=False)
        symbol = PriceFormatter._CURRENCY_SYMBOLS.get('USD', 'USD ')
        if symbol.isalpha():  # e.g., 'CHF' or 'USDT'
            return f'{symbol} {number_str}'
        return f'{symbol}{number_str}'

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        '''
        Format quantity for display.
        Args:
            quantity: Quantity value to format
        Returns:
            Formatted quantity string
        '''
        d = PriceFormatter._to_decimal(quantity)
        if d is None:
            return 'N/A'
        # If it's effectively an integer, show no decimals; otherwise up to 6 decimals
        if d == d.to_integral():
            return PriceFormatter._group_number_str(format(d.quantize(Decimal(1), rounding=ROUND_HALF_UP), 'f'))
        # Up to 6 decimals, trimmed
        return PriceFormatter._format_decimal(d, max_frac=6, min_frac=0, grouping=True, trim_trailing_zeros=True)

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        '''
        Format percentage for display.
        Args:
            percentage: Percentage value to format (as decimal, e.g., 0.05 for 5%)
        Returns:
            Formatted percentage string
        '''
        d = PriceFormatter._to_decimal(percentage)
        if d is None:
            return 'N/A'
        pct = d * Decimal(100)
        # Show up to 2 decimals, trimmed
        s = PriceFormatter._format_decimal(
            pct, max_frac=2, min_frac=0, grouping=True, trim_trailing_zeros=True)
        return f'{s}%'

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
        d = PriceFormatter._to_decimal(price)
        if d is None:
            return 'N/A'
        abs_d = abs(d)
        if abs_d < Decimal('1'):
            # Show more precision for small prices
            return PriceFormatter._format_decimal(d, max_frac=6, min_frac=0, grouping=True, trim_trailing_zeros=True)
        else:
            # Typical currency style
            return PriceFormatter._format_decimal(d, max_frac=2, min_frac=0, grouping=True, trim_trailing_zeros=True)

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
        d = PriceFormatter._to_decimal(price)
        if d is None:
            return 'N/A'
        code = (currency or 'USD').upper()
        decimals = PriceFormatter._CURRENCY_DECIMALS.get(code, 2)
        symbol = PriceFormatter._CURRENCY_SYMBOLS.get(code, code)
        number_str = PriceFormatter._format_decimal(
            d, max_frac=decimals, min_frac=decimals, grouping=True, trim_trailing_zeros=False)

        # If symbol looks like a code (alphabetic), place a space between code and number.
        if symbol.isalpha():
            return f'{symbol} {number_str}'
        return f'{symbol}{number_str}'
