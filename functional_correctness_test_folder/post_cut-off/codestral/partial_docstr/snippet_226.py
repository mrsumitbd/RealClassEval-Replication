
from typing import Union


class PriceFormatter:

    @staticmethod
    def format_price_for_display(price: Union[float, int, None], force_precision: int = None) -> str:
        if price is None:
            return "N/A"
        if force_precision is not None:
            return f"{price:.{force_precision}f}"
        return f"{price:.2f}" if isinstance(price, float) else str(price)

    @staticmethod
    def format_price_for_logging(price: Union[float, int, None]) -> str:
        if price is None:
            return "null"
        return str(price)

    @staticmethod
    def format_quantity(quantity: Union[float, int, None]) -> str:
        if quantity is None:
            return "N/A"
        return f"{quantity:.2f}" if isinstance(quantity, float) else str(quantity)

    @staticmethod
    def format_percentage(percentage: Union[float, int, None]) -> str:
        if percentage is None:
            return "N/A"
        return f"{percentage * 100:.2f}%"

    @staticmethod
    def format_currency(price: Union[float, int, None], currency: str = 'USD') -> str:
        if price is None:
            return "N/A"
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'BTC': '₿',
            'GBP': '£',
            'JPY': '¥',
            'CNY': '¥',
            'INR': '₹',
            'RUB': '₽',
            'AUD': 'A$',
            'CAD': 'C$',
            'CHF': 'CHF',
            'NZD': 'NZ$',
            'SEK': 'kr',
            'NOK': 'kr',
            'DKK': 'kr',
            'TRY': '₺',
            'ZAR': 'R',
            'BRL': 'R$',
            'MXN': 'Mex$',
            'SGD': 'S$',
            'HKD': 'HK$',
            'TWD': 'NT$',
            'THB': '฿',
            'MYR': 'RM',
            'PHP': '₱',
            'IDR': 'Rp',
            'VND': '₫',
            'KRW': '₩',
            'ILS': '₪',
            'PLN': 'zł',
            'HUF': 'Ft',
            'CZK': 'Kč',
            'RON': 'lei',
            'BGN': 'лв',
            'HRK': 'kn',
            'ISK': 'kr',
            'LTL': 'Lt',
            'LVL': 'Ls',
            'MTL': '₤',
            'SKK': 'Sk',
            'SIT': 'SIT',
            'EEK': 'kr',
            'MKD': 'ден',
            'ALL': 'Lek',
            'AMD': '֏',
            'AZN': '₼',
            'BYN': 'Br',
            'GEL': '₾',
            'KGS': 'лв',
            'MDL': 'L',
            'TMT': 'm',
            'UAH': '₴',
            'UZS': 'лв',
            'KZT': '₸',
            'AFN': '؋',
            'BDT': '৳',
            'BTN': 'Nu.',
            'NPR': '₨',
            'PKR': '₨',
            'LKR': '₨',
            'MVR': 'Rf',
            'SCR': '₨',
            'BND': 'B$',
            'FJD': 'FJ$',
            'KWD': 'KD',
            'OMR': 'OMR',
            'QAR': 'QR',
            'SAR': 'SR',
            'YER': 'YR',
            'AED': 'د.إ',
            'BHD': 'BD',
            'JOD': 'JD',
            'LYD': 'LD',
            'SYP': '£S',
            'IQD': 'IQD',
            'IRR': '﷼',
            'EGP': 'E£',
            'DZD': 'DA',
            'MAD': 'DH',
            'TND': 'DT',
            'SDG': 'SDG',
            'SOS': 'S',
            'ETB': 'Br',
            'DJF': 'Fdj',
            'GHS': 'GH₵',
            'XOF': 'CFA',
            'XAF': 'FCFA',
            'XPF': '₣',
            'MGA': 'Ar',
            'MUR': '₨',
            'MWK': 'MK',
            'ZMW': 'ZK',
            'NAD': 'N$',
            'NGN': '₦',
            'SLL': 'Le',
            'SZL': 'E',
            'TZS': 'TSh',
            'UGX': 'USh',
            'ZWL': 'Z$',
            'CLP': 'CLP$',
            'COP': 'COL$',
            'PEN': 'S/',
            'ARS': 'AR$',
            'BOB': 'Bs',
            'PYG': '₲',
            'UYU': '$U',
            'VEF': 'Bs.F',
            'CRC': '₡',
            'DOP': 'RD$',
            'GTQ': 'Q',
            'HNL': 'L',
            'NIO': 'C$',
            'PAB': 'B/.',
            'TTD': 'TT$',
            'BSD': 'B$',
            'BZD': 'BZ$',
            'BMD': 'BD$',
            'KYD': 'CI$',
            'ANG': 'NAf',
            'AWG': 'Afl',
            'BBD': 'Bds$',
            'BMD': 'BD$',
            'BND': 'B$',
            'BZD': 'BZ$',
            'FJD': 'FJ$',
            'GYD': 'G$',
            'JMD': 'J$',
            'KYD': 'CI$',
            'LRD': 'L$',
            'NAD': 'N$',
            'SBD': 'SI$',
            'SRD': 'SRD',
            'TOP': 'T$',
            'VUV': 'VT',
            'WST': 'WS$',
            'XCD': 'EC$',
            'ZWD': 'Z$',
        }
        symbol = currency_symbols.get(currency, currency)
        formatted_price = PriceFormatter.format_price_for_display(price)
        return f"{symbol}{formatted_price}"
