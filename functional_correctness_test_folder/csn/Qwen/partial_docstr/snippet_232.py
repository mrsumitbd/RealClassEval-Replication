
import pandas as pd
from typing import Sequence, Dict, Tuple, List


class Order0Interp:
    '''A callable that returns the result of order 0 interpolation over input data.
    Attributes
    ----------
    data
        The data from which to build the interpolation.
    value_columns
        Columns to be interpolated.
    extrapolate
        Whether or not to extrapolate beyond the edge of supplied bins.
    parameter_bins
        A dictionary where they keys are a tuple of the form
        (column name used in call, column name for left bin edge, column name for right bin edge)
        and the values are dictionaries of the form {"bins": [ordered left edges of bins],
        "max": max right edge (used when extrapolation not allowed)}.
    '''

    def __init__(self, data: pd.DataFrame, continuous_parameters: Sequence[Sequence[str]], value_columns: list[str], extrapolate: bool, validate: bool):
        self.data = data
        self.value_columns = value_columns
        self.extrapolate = extrapolate
        self.parameter_bins = {}

        for param in continuous_parameters:
            col_name, left_bin, right_bin = param
            bins = sorted(data[left_bin].unique())
            max_val = data[right_bin].max()
            self.parameter_bins[(col_name, left_bin, right_bin)] = {
                "bins": bins, "max": max_val}

        if validate:
            self._validate()

    def _validate(self):
        for (col_name, left_bin, right_bin), bin_info in self.parameter_bins.items():
            if not all(self.data[right_bin] >= self.data[left_bin]):
                raise ValueError(
                    f"Right bin values must be greater than or equal to left bin values for {col_name}.")
            if not self.data[col_name].isin(bin_info["bins"]).all():
                raise ValueError(
                    f"All values in {col_name} must be present in the left bin edges.")

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        '''Find the bins for each parameter for each interpolant in interpolants
        and return the values from data there.
        Parameters
        ----------
        interpolants
            Data frame containing the parameters to interpolate..
        Returns
        -------
            A table with the interpolated values for the given interpolants.
        '''
        results = interpolants.copy()

        for (col_name, left_bin, right_bin), bin_info in self.parameter_bins.items():
            bins = bin_info["bins"]
            max_val = bin_info["max"]

            def find_bin(value):
                if value < bins[0]:
                    return bins[0] if self.extrapolate else None
                elif value > max_val:
                    return bins[-1] if self.extrapolate else None
                else:
                    return bins[bisect.bisect_left(bins, value) - 1]

            results[col_name] = results[col_name].apply(find_bin)

        merged = pd.merge(results, self.data, left_on=[col for _, left_bin, _ in self.parameter_bins.values()],
                          right_on=[left_bin for _, left_bin, _ in self.parameter_bins.values()], how='left')

        return merged[self.value_columns]
