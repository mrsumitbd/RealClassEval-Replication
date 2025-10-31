from typing import Union
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


class PriceFormatter:
    '''Utility class for formatting prices and quantities consistently.'''

    @staticmethod
    def _to_decimal(value: Union[float, int]) -> Decimal:
        try:
            # Use string conversion to avoid binary float artifacts
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            return Decimal(0)

    @staticmethod
    def _format_number(value: Decimal, *, max_decimals: int, min_decimals: int = 0, grouping: bool = True) -> str:
        sign = '-' if value < 0 else ''
        abs_val = -value if value < 0 else value

        if max_decimals <= 0:
            quant = Decimal('1')
        else:
            quant = Decimal(1).scaleb(-max_decimals)  # 10 ** -max_decimals

        q = abs_val.quantize(quant, rounding=ROUND_HALF_UP)
        fmt = f"{{:,.{max_decimals}f}}" if grouping else f"{{:.{max_decimals}f}}"
        s = fmt.format(q)

        # Strip trailing zeros but keep at least min_decimals
        if max_decimals > 0:
            if '.' in s:
                int_part, dec_part = s.split('.')
                dec_part = dec_part.rstrip('0')
                if len(dec_part) < min_decimals:
                    dec_part = dec_part + \
                        ('0' * (min_decimals - len(dec_part)))
                s = int_part if dec_part == '' else f"{int_part}.{dec_part}"

        return f"{sign}{s}"

    @staticmethod
    def _decimals_for_display(amount: Decimal) -> int:
        a = abs(amount)
        if a >= Decimal('1'):
            return 2
        if a >= Decimal('0.1'):
            return 4
        if a >= Decimal('0.01'):
            return 6
        return 8

    @staticmethod
    def _decimals_for_logging(amount: Decimal) -> int:
        a = abs(amount)
        if a >= Decimal('1'):
            return 6
        if a >= Decimal('0.01'):
            return 8
        return 12

    @staticmethod
    def _map_currency(currency: str) -> tuple[str, str]:
        # returns (symbol_or_code, position) where position is 'prefix' or 'suffix'
        cur = (currency or '').upper()
        mapping = {
            'USD': ('$', 'prefix'),
            'EUR': ('€', 'prefix'),
            'GBP': ('£', 'prefix'),
            'JPY': ('¥', 'prefix'),
            'CNY': ('¥', 'prefix'),
            'KRW': ('₩', 'prefix'),
            'INR': ('₹', 'prefix'),
            'BTC': ('₿', 'prefix'),
            'ETH': ('Ξ', 'prefix'),
        }
        return mapping.get(cur, (cur or 'USD', 'suffix' if len(cur) == 3 else 'prefix'))

    @staticmethod
    def _apply_currency(formatted_number: str, currency: str) -> str:
        symbol, position = PriceFormatter._map_currency(currency)
        # Keep negative sign nearest to the number
        if formatted_number.startswith('-'):
            core = formatted_number[1:]
            if position == 'prefix' and symbol and len(symbol) == 1 and not symbol.isalpha():
                return f"-{symbol}{core}"
            if position == 'prefix':
                return f"-{symbol}{core}" if symbol and symbol != currency else f"-{core} {symbol}"
            else:
                return f"-{core}{symbol}" if symbol and len(symbol) == 1 and not symbol.isalpha() else f"-{core} {symbol}"
        else:
            if position == 'prefix' and symbol and len(symbol) == 1 and not symbol.isalpha():
                return f"{symbol}{formatted_number}"
            if position == 'prefix':
                return f"{symbol}{formatted_number}" if symbol and symbol != currency else f"{formatted_number} {symbol}"
            else:
                return f"{formatted_number}{symbol}" if symbol and len(symbol) == 1 and not symbol.isalpha() else f"{formatted_number} {symbol}"

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
            return '-'
        dec = PriceFormatter._to_decimal(price)
        max_dec = PriceFormatter._decimals_for_display(dec)
        return PriceFormatter._format_number(dec, max_decimals=max_dec, min_decimals=0, grouping=True)

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
            return '-'
        dec = PriceFormatter._to_decimal(price)
        max_dec = PriceFormatter._decimals_for_logging(dec)
        num = PriceFormatter._format_number(
            dec, max_decimals=max_dec, min_decimals=0, grouping=True)
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
        if quantity is None:
            return '-'
        dec = PriceFormatter._to_decimal(quantity)
        # Treat near-integers as integers
        if dec == dec.to_integral_value(rounding=ROUND_HALF_UP):
            return PriceFormatter._format_number(dec, max_decimals=0, grouping=True)
        # Otherwise show up to 4 decimals for readability
        return PriceFormatter._format_number(dec, max_decimals=4, min_decimals=0, grouping=True)

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
            return '-'
        dec = PriceFormatter._to_decimal(percentage) * Decimal('100')
        abs_dec = abs(dec)
        if abs_dec >= Decimal('1'):
            max_dec = 2
        elif abs_dec >= Decimal('0.1'):
            max_dec = 2
        else:
            max_dec = 4
        s = PriceFormatter._format_number(
            dec, max_decimals=max_dec, min_decimals=0, grouping=True)
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
        if price is None:
            return '-'
        dec = PriceFormatter._to_decimal(price)
        max_dec = PriceFormatter._decimals_for_display(dec)
        num = PriceFormatter._format_number(
            dec, max_decimals=max_dec, min_decimals=0, grouping=True)
        return PriceFormatter._apply_currency(num, currency)
