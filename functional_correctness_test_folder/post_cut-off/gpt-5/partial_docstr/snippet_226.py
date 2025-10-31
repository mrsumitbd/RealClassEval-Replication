from decimal import Decimal, InvalidOperation, localcontext
from typing import Union


class PriceFormatter:
    @staticmethod
    def _to_decimal(value: Union[float, int]) -> Decimal:
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            return Decimal(0)

    @staticmethod
    def _trimmed_str(d: Decimal, max_decimals: int | None = None, min_decimals: int = 0) -> str:
        if max_decimals is not None:
            with localcontext() as ctx:
                # Increase precision to avoid rounding issues when quantizing
                ctx.prec = max(28, max_decimals + 10)
                q = Decimal(1).scaleb(-max_decimals)  # 10^-max_decimals
                d = d.quantize(q)
        s = format(d.normalize(), 'f')
        if '.' in s:
            # Ensure minimum decimals
            int_part, frac_part = s.split('.', 1)
            frac_part = frac_part.rstrip('0')
            if min_decimals > 0:
                frac_part = frac_part.ljust(min_decimals, '0')
            s = int_part if frac_part == '' else f"{int_part}.{frac_part}"
        else:
            if min_decimals > 0:
                s = f"{s}.{''.ljust(min_decimals, '0')}"
        return s

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        if price is None:
            return '-'
        d = PriceFormatter._to_decimal(price)
        return PriceFormatter._trimmed_str(d)

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        if price is None:
            return 'None'
        d = PriceFormatter._to_decimal(price)
        return PriceFormatter._trimmed_str(d, max_decimals=10)

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        if quantity is None:
            return '-'
        d = PriceFormatter._to_decimal(quantity)
        # Up to 8 decimals, no forced trailing zeros
        return PriceFormatter._trimmed_str(d, max_decimals=8)

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
        d = PriceFormatter._to_decimal(percentage) * Decimal(100)
        abs_d = abs(d)
        if abs_d >= 1:
            s = PriceFormatter._trimmed_str(d, max_decimals=2)
        else:
            s = PriceFormatter._trimmed_str(d, max_decimals=4)
        return f"{s}%"

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
        d = PriceFormatter._to_decimal(price)
        return PriceFormatter._trimmed_str(d)

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
        currency_upper = (currency or '').upper()

        fiat_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CNY': '¥',
            'INR': '₹',
            'AUD': 'A$',
            'CAD': 'C$',
            'CHF': 'CHF',
        }
        crypto_symbols = {
            'BTC': '₿',
            'ETH': 'Ξ',
            'USDT': '₮',
            'USDC': '∮',  # placeholder symbol; many stablecoins lack unique symbols
        }

        d = PriceFormatter._to_decimal(price)

        if currency_upper in fiat_symbols:
            symbol = fiat_symbols[currency_upper]
            # Force 2 decimals for fiat
            s = PriceFormatter._trimmed_str(d, max_decimals=2, min_decimals=2)
            return f"{symbol}{s}"
        elif currency_upper in crypto_symbols:
            symbol = crypto_symbols[currency_upper]
            # Up to 8 decimals for crypto, no forced trailing zeros
            s = PriceFormatter._trimmed_str(d, max_decimals=8)
            return f"{symbol}{s}"
        else:
            # Fallback: show code after amount, up to 8 decimals trimmed
            s = PriceFormatter._trimmed_str(d, max_decimals=8)
            return f"{s} {currency_upper if currency_upper else ''}".strip()
