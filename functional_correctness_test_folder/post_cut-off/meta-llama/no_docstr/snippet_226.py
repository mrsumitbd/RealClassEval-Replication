
from typing import Union


class PriceFormatter:

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        if price is None:
            return 'N/A'
        return f'${price:,.2f}'

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        if price is None:
            return 'None'
        return str(price)

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        if quantity is None:
            return 'N/A'
        return f'{quantity:,.4f}'

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        if percentage is None:
            return 'N/A'
        return f'{percentage:.2f}%'

    @staticmethod
    def format_currency(price: Union[float, int, None], currency: str = 'USD') -> str:
        if price is None:
            return 'N/A'
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CNY': 'CN¥'
        }
        symbol = currency_symbols.get(currency, '')
        return f'{symbol}{price:,.2f} {currency}'
