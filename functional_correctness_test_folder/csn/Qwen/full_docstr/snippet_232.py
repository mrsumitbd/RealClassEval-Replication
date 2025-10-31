
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

    def __init__(self, data: pd.DataFrame, continuous_parameters: Sequence[Sequence[str]], value_columns: List[str], extrapolate: bool, validate: bool):
        '''
        Parameters
        ----------
        data
            Data frame used to build interpolation.
        continuous_parameters
            Parameter columns. Should be of form (column name used in call,
            column name for left bin edge, column name for right bin edge)
            or column name. Assumes left bin edges are inclusive and
            right exclusive.
        value_columns
            Columns to be interpolated.
        extrapolate
            Whether or not to extrapolate beyond the edge of supplied bins.
        validate
            Whether or not to validate the data.
        '''
        self.data = data
        self.value_columns = value_columns
        self.extrapolate = extrapolate
        self.parameter_bins = {}

        for param in continuous_parameters:
            if isinstance(param, str):
                left_bin_col = f"{param}_left"
                right_bin_col = f"{param}_right"
            else:
                param, left_bin_col, right_bin_col = param

            bins = sorted(self.data[left_bin_col].unique())
            max_right = self.data[right_bin_col].max()
            self.parameter_bins[(param, left_bin_col, right_bin_col)] = {
                "bins": bins, "max": max_right}

        if validate:
            self._validate()

    def _validate(self):
        for param, left_bin_col, right_bin_col in self.parameter_bins:
            if not all(self.data[left_bin_col] <= self.data[right_bin_col]):
                raise ValueError(
                    f"Left bin edges must be less than or equal to right bin edges for {param}.")
            if not self.data[left_bin_col].is_monotonic_increasing:
                raise ValueError(
                    f"Left bin edges must be monotonic increasing for {param}.")

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

        for param, left_bin_col, right_bin_col in self.parameter_bins:
            bins = self.parameter_bins[(
                param, left_bin_col, right_bin_col)]["bins"]
            max_right = self.parameter_bins[(
                param, left_bin_col, right_bin_col)]["max"]

            def find_bin(x):
                idx = pd.IntervalIndex.from_breaks(
                    bins + [max_right], closed='left').get_loc(x)
                if idx < 0 or idx >= len(bins):
                    if not self.extrapolate:
                        raise ValueError(
                            f"Value {x} for {param} is out of bounds and extrapolation is not allowed.")
                    idx = max(0, min(len(bins) - 1, idx))
                return idx

            results[f"{param}_bin"] = results[param].apply(find_bin)

        merged = pd.merge_asof(
            results.sort_values(param),
            self.data.sort_values(left_bin_col),
            left_on=param,
            right_on=left_bin_col,
            direction='forward' if self.extrapolate else 'nearest'
        )

        return merged[results.columns.tolist() + self.value_columns]
