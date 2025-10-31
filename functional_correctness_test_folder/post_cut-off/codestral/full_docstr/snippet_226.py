
from typing import Union


class PriceFormatter:
    '''Utility class for formatting prices and quantities consistently.'''
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
            return "N/A"
        return f"${price:,.2f}"

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
            return "N/A"
        return f"${price:,.4f}"

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
            return "N/A"
        return f"{quantity:,.2f}"

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
            return "N/A"
        return f"{percentage:.2%}"

    @staticmethod
    def format_price_without_currency(price: Union[float, int, None], force_precision: int = None) -> str:
        '''
        Format price without currency symbol, preserving precision.
        Args:
            price: Price value to format
            force_precision: Optional forced decimal places
        Returns:
            Formatted price string without currency symbol
        '''
        if price is None:
            return "N/A"
        if force_precision is not None:
            return f"{price:.{force_precision}f}"
        return f"{price:,.2f}"

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
            'KRW': '₩',
            'TRY': '₺',
            'AUD': 'A$',
            'CAD': 'C$',
            'CHF': 'CHF',
            'NZD': 'NZ$',
            'SEK': 'kr',
            'NOK': 'kr',
            'DKK': 'kr',
            'PLN': 'zł',
            'ZAR': 'R',
            'MXN': 'Mex$',
            'SGD': 'S$',
            'HKD': 'HK$',
            'TWD': 'NT$',
            'THB': '฿',
            'MYR': 'RM',
            'PHP': '₱',
            'IDR': 'Rp',
            'VND': '₫',
            'ILS': '₪',
            'AED': 'د.إ',
            'SAR': '﷼',
            'EGP': 'E£',
            'KWD': 'د.ك',
            'BHD': 'د.ب',
            'OMR': 'ر.ع.',
            'QAR': 'ر.ق',
            'JOD': 'د.ا',
            'LBP': 'ل.ل',
            'DZD': 'د.ج',
            'TND': 'د.ت',
            'MAD': 'د.م.',
            'ARS': '$',
            'CLP': '$',
            'COP': '$',
            'PEN': 'S/',
            'BRL': 'R$',
            'PYG': '₲',
            'UYU': '$U',
            'BOB': 'Bs',
            'CRC': '₡',
            'DOP': 'RD$',
            'GTQ': 'Q',
            'HNL': 'L',
            'NIO': 'C$',
            'PAB': 'B/.',
            'PYG': '₲',
            'UYU': '$U',
            'VEF': 'Bs',
            'XAF': 'FCFA',
            'XOF': 'CFA',
            'XPF': '₣',
            'ZMW': 'ZK',
            'ZWL': 'Z$',
            'BWP': 'P',
            'GHS': '₵',
            'KES': 'KSh',
            'NGN': '₦',
            'UGX': 'USh',
            'TZS': 'TSh',
            'ETB': 'Br',
            'MZN': 'MT',
            'AOA': 'Kz',
            'NAD': 'N$',
            'ZAR': 'R',
            'MWK': 'MK',
            'SZL': 'E',
            'LSL': 'L',
            'BIF': 'FBu',
            'RWF': 'RF',
            'CDF': 'FC',
            'SSP': '£',
            'SDG': 'ج.س.',
            'SYP': '£S',
            'IQD': 'ع.د',
            'YER': '﷼',
            'LYD': 'ل.د',
            'TND': 'د.ت',
            'DZD': 'د.ج',
            'MAD': 'د.م.',
            'MUR': '₨',
            'SCR': '₨',
            'LKR': '₨',
            'NPR': '₨',
            'PKR': '₨',
            'BDT': '৳',
            'MMK': 'K',
            'KHR': '៛',
            'LAK': '₭',
            'KPW': '₩',
            'AFN': '؋',
            'IRR': '﷼',
            'BYN': 'Br',
            'UAH': '₴',
            'GEL': '₾',
            'AZN': '₼',
            'KGS': 'лв',
            'TMT': 'm',
            'UZS': 'лв',
            'KZT': '₸',
            'AMD': '֏',
            'GMD': 'D',
            'SLL': 'Le',
            'GNF': 'FG',
            'XAG': 'XAG',
            'XAU': 'XAU',
            'XPD': 'XPD',
            'XPT': 'XPT',
            'XRH': 'XRH',
            'XTC': 'XTC',
            'XRP': 'XRP',
            'XLM': 'XLM',
            'XEM': 'XEM',
            'XMR': 'XMR',
            'XZC': 'XZC',
            'DASH': 'DASH',
            'LTC': 'Ł',
            'DOGE': 'Ð',
            'ETH': 'Ξ',
            'BTC': '₿',
            'XBT': '₿',
            'BCH': 'BCH',
            'ETC': 'ETC',
            'ZEC': 'ZEC',
            'XVG': 'XVG',
            'STRAT': 'STRAT',
            'MONA': 'MONA',
            'FCT': 'FCT',
            'RDD': 'RDD',
            'POT': 'POT',
            'GAME': 'GAME',
            'GRC': 'GRC',
            'DGB': 'DGB',
            'EXP': 'EXP',
            'FLO': 'FLO',
            'CLAM': 'CLAM',
            'VTC': 'VTC',
            'VIA': 'VIA',
            'XPM': 'XPM',
            'BLK': 'BLK',
            'NEOS': 'NEOS',
            'XDN': 'XDN',
            'PPC': 'PPC',
            'DCR': 'DCR',
            'EMC2': 'EMC2',
            'XRP': 'XRP',
            'XLM': 'XLM',
            'XEM': 'XEM',
            'XMR': 'XMR',
            'XZC': 'XZC',
            'DASH': 'DASH',
            'LTC': 'Ł',
            'DOGE': 'Ð',
            'ETH': 'Ξ',
            'BTC': '₿',
            'XBT': '₿',
            'BCH': 'BCH',
            'ETC': 'ETC',
            'ZEC': 'ZEC',
            'XVG': 'XVG',
            'STRAT': 'STRAT',
            'MONA': 'MONA',
            'FCT': 'FCT',
            'RDD': 'RDD',
            'POT': 'POT',
            'GAME': 'GAME',
            'GRC': 'GRC',
            'DGB': 'DGB',
            'EXP': 'EXP',
            'FLO': 'FLO',
            'CLAM': 'CLAM',
            'VTC': 'VTC',
            'VIA': 'VIA',
            'XPM': 'XPM',
            'BLK': 'BLK',
            'NEOS': 'NEOS',
            'XDN': 'XDN',
            'PPC': 'PPC',
            'DCR': 'DCR',
            'EMC2': 'EMC2',
        }
        symbol = currency_symbols.get(currency, currency)
        return f"{symbol}{price:,.2f}"
