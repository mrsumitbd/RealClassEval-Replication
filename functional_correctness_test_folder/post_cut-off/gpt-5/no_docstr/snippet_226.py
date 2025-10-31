from typing import Union


class PriceFormatter:
    @staticmethod
    def _strip_trailing_zeros(s: str) -> str:
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return s

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        if price is None:
            return "-"
        try:
            return f"{float(price):,.2f}"
        except (ValueError, TypeError):
            return "-"

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        if price is None:
            return "None"
        return str(price)

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        if quantity is None:
            return "-"
        try:
            if isinstance(quantity, int):
                return str(quantity)
            s = f"{float(quantity):.4f}"
            return PriceFormatter._strip_trailing_zeros(s)
        except (ValueError, TypeError):
            return "-"

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        if percentage is None:
            return "-"
        try:
            return f"{float(percentage):.2f}%"
        except (ValueError, TypeError):
            return "-"

    @staticmethod
    def format_currency(price: Union[float, int, None], currency: str = "USD") -> str:
        if price is None:
            return "-"
        try:
            amount = f"{float(price):,.2f}"
        except (ValueError, TypeError):
            return "-"

        code = (currency or "").upper()
        mapping = {
            "USD": ("$", ""),
            "EUR": ("€", ""),
            "GBP": ("£", ""),
            "JPY": ("¥", ""),
            "CNY": ("¥", ""),
            "INR": ("₹", ""),
            "KRW": ("₩", ""),
            "RUB": ("₽", ""),
            "TRY": ("₺", ""),
            "BRL": ("R$", ""),
            "AUD": ("A$", ""),
            "CAD": ("C$", ""),
            "HKD": ("HK$", ""),
            "SGD": ("S$", ""),
            "NZD": ("NZ$", ""),
            "MXN": ("Mex$", ""),
            "ZAR": ("R", ""),
            "CHF": ("CHF ", ""),
            "SEK": ("kr ", ""),
            "NOK": ("kr ", ""),
            "DKK": ("kr ", ""),
        }

        prefix, suffix = mapping.get(code, ("", f" {code}" if code else ""))
        return f"{prefix}{amount}{suffix}"
