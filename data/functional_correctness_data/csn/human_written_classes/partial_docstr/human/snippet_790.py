import pandas
from physt.types import Histogram1D, Histogram2D, HistogramND
import warnings
from pandas.api.types import is_numeric_dtype
from physt._construction import calculate_1d_bins, extract_1d_array, extract_nd_array
import pandas as pd
from physt._facade import h, h1

@pandas.api.extensions.register_series_accessor('physt')
class PhystSeriesAccessor:
    """Histogramming methods for pandas Series.

    It exists only for numeric series.
    """

    def __init__(self, series: pandas.Series):
        if not is_numeric_dtype(series):
            raise AttributeError(f'Series must be of a numeric type, not {series.dtype}')
        self._series = series

    def h1(self, bins=None, **kwargs) -> Histogram1D:
        """Create a histogram from the series."""
        return h1(self._series, bins=bins, **kwargs)
    histogram = h1

    def cut(self, bins=None, **kwargs) -> pd.Series:
        """Bin values using physt binning (eq. to pd.cut)."""
        warnings.warn('This method is experimental, only partially implemented and may removed.')
        binning = calculate_1d_bins(extract_1d_array(self._series, dropna=True)[0], bins, **kwargs)
        return pd.cut(self._series, binning.numpy_bins)