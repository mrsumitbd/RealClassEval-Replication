from yfinance import utils, const
from yfinance.data import YfData
from yfinance.exceptions import YFException, YFNotImplementedError
import warnings
import pandas as pd

class Fundamentals:

    def __init__(self, data: YfData, symbol: str, proxy=const._SENTINEL_):
        if proxy is not const._SENTINEL_:
            warnings.warn('Set proxy via new config function: yf.set_config(proxy=proxy)', DeprecationWarning, stacklevel=2)
            data._set_proxy(proxy)
        self._data = data
        self._symbol = symbol
        self._earnings = None
        self._financials = None
        self._shares = None
        self._financials_data = None
        self._fin_data_quote = None
        self._basics_already_scraped = False
        self._financials = Financials(data, symbol)

    @property
    def financials(self) -> 'Financials':
        return self._financials

    @property
    def earnings(self) -> dict:
        warnings.warn('\'Ticker.earnings\' is deprecated as not available via API. Look for "Net Income" in Ticker.income_stmt.', DeprecationWarning)
        return None

    @property
    def shares(self) -> pd.DataFrame:
        if self._shares is None:
            raise YFNotImplementedError('shares')
        return self._shares