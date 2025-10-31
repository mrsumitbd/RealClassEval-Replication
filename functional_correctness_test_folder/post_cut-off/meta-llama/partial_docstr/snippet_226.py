
from typing import Union


class PriceFormatter:

    @staticmethod
    def format_price_for_display(price: Union[float, int, None]) -> str:
        if price is None:
            return 'N/A'
        return '{:.2f}'.format(price)

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        if price is None:
            return 'None'
        return str(price)

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        if quantity is None:
            return 'N/A'
        return '{:.8f}'.format(quantity)

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        if percentage is None:
            return 'N/A'
        return '{:.2f}%'.format(percentage * 100)

    @staticmethod
    def format_currency(price: Union[float, int, None], currency: str = 'USD') -> str:
        if price is None:
            return 'N/A'
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'CNY': 'CN¥',
            'BTC': '₿'
        }
        symbol = currency_symbols.get(currency.upper(), currency.upper())
        return '{}{:.2f}'.format(symbol, price)


# Example usage:
if __name__ == "__main__":
    print(PriceFormatter.format_price_for_display(10.1234))  # Output: 10.12
    print(PriceFormatter.format_price_for_logging(10.1234))  # Output: 10.1234
    print(PriceFormatter.format_quantity(0.00001234))  # Output: 0.00001234
    print(PriceFormatter.format_percentage(0.05))  # Output: 5.00%
    print(PriceFormatter.format_currency(10.1234, 'USD'))  # Output: $10.12
    print(PriceFormatter.format_currency(10.1234, 'EUR'))  # Output: €10.12
    print(PriceFormatter.format_currency(10.1234, 'BTC'))  # Output: ₿10.12
