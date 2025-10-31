from typing import Union
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


class PriceFormatter:
    '''Utility class for formatting prices and quantities consistently.'''

    _CURRENCY_SYMBOLS = {
        'USD': ('$', 'prefix'),
        'EUR': ('€', 'prefix'),
        'GBP': ('£', 'prefix'),
        'JPY': ('¥', 'prefix'),
        'CNY': ('¥', 'prefix'),
        'INR': ('₹', 'prefix'),
        'BTC': ('₿', 'prefix'),
        'ETH': ('Ξ', 'prefix'),
        'AUD': ('A$', 'prefix'),
        'CAD': ('C$', 'prefix'),
        'CHF': ('CHF', 'suffix'),
        'HKD': ('HK$', 'prefix'),
        'SGD': ('S$', 'prefix'),
        'KRW': ('₩', 'prefix'),
        'RUB': ('₽', 'prefix'),
        'MXN': ('MX$', 'prefix'),
        'BRL': ('R$', 'prefix'),
        'ZAR': ('R', 'prefix'),
    }

    @staticmethod
    def _to_decimal(value: Union[float, int, None]) -> Decimal | None:
        if value is None:
            return None
        try:
            if isinstance(value, Decimal):
                dec = value
            else:
                dec = Decimal(str(value))
            # Normalize -0 to 0
            if dec == 0:
                dec = Decimal('0')
            return dec
        except (InvalidOperation, ValueError, TypeError):
            return None

    @staticmethod
    def _format_number(dec: Decimal, *, min_dp: int, max_dp: int, group: bool = True) -> str:
        if max_dp < min_dp:
            max_dp = min_dp
        # Quantize to max precision first
        quant = Decimal('1') if max_dp == 0 else Decimal('1.' + ('0' * max_dp))
        q = dec.quantize(quant, rounding=ROUND_HALF_UP)
        # Handle "-0.00" -> "0.00"
        if q == 0:
            q = abs(q)
        s = format(q, 'f')
        sign = ''
        if s.startswith('-'):
            sign = '-'
            s = s[1:]
        if '.' in s:
            int_part, frac = s.split('.', 1)
            # Trim trailing zeros down to min_dp
            while len(frac) > min_dp and frac.endswith('0'):
                frac = frac[:-1]
        else:
            int_part, frac = s, ''
        if group:
            # Safely group integer part
            try:
                grouped = f"{int(int_part):,}"
            except ValueError:
                grouped = int_part  # fallback
        else:
            grouped = int_part
        if frac or min_dp > 0:
            if len(frac) < min_dp:
                frac = frac + ('0' * (min_dp - len(frac)))
            number = f"{grouped}.{frac}"
        else:
            number = grouped
        return f"{sign}{number}"

    @staticmethod
    def _apply_currency(number_str: str, currency: str) -> str:
        if not number_str:
            return number_str
        sign = ''
        if number_str.startswith('-'):
            sign = '-'
            number_str = number_str[1:]
        sym, pos = PriceFormatter._CURRENCY_SYMBOLS.get(
            currency.upper(), (currency.upper(), 'suffix'))
        if len(sym) == 1 and sym.isalpha():
            # If fallback symbol is like 'X', treat as code suffix
            sym, pos = currency.upper(), 'suffix'
        if pos == 'prefix' and len(sym) > 1 and sym.isalpha():
            # Codes like 'CHF' often better as suffix "123.45 CHF"
            pos = 'suffix'
        if pos == 'prefix' and not sym.isalpha():
            result = f"{sign}{sym}{number_str}"
        elif pos == 'prefix':
            result = f"{sign}{sym} {number_str}"
        else:
            result = f"{sign}{number_str} {sym}"
        return result.strip()

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
        if abs_dec >= Decimal('1'):
            # Standard price formatting for >= 1: 2 decimal places
            return PriceFormatter._format_number(dec, min_dp=2, max_dp=2, group=True)
        # For small prices, allow more precision (up to 8), keep at least 2
        # Example: 0.12345678 -> 0.12345678, 0.1 -> 0.10
        return PriceFormatter._format_number(dec, min_dp=2, max_dp=8, group=True)

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
        abs_dec = abs(dec)
        if abs_dec >= Decimal('1'):
            num = PriceFormatter._format_number(
                dec, min_dp=4, max_dp=8, group=True)
        else:
            num = PriceFormatter._format_number(
                dec, min_dp=6, max_dp=10, group=True)
        return PriceFormatter._apply_currency(num, 'USD')

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
        abs_dec = abs(dec)
        if dec == dec.to_integral_value():
            return PriceFormatter._format_number(dec, min_dp=0, max_dp=0, group=True)
        if abs_dec >= Decimal('1'):
            return PriceFormatter._format_number(dec, min_dp=0, max_dp=4, group=True)
        return PriceFormatter._format_number(dec, min_dp=0, max_dp=8, group=True)

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
        abs_pct = abs(pct)
        if abs_pct >= Decimal('1'):
            num = PriceFormatter._format_number(
                pct, min_dp=0, max_dp=2, group=False)
        else:
            num = PriceFormatter._format_number(
                pct, min_dp=2, max_dp=4, group=False)
        return f"{num}%"

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
        num = PriceFormatter.format_price_for_display(price)
        if num == '-':
            return num
        return PriceFormatter._apply_currency(num, currency)
