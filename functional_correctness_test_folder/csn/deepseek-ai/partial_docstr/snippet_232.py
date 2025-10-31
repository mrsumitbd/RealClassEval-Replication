
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
        self.parameter_bins: Dict[Tuple[str, str, str], Dict] = {}

        for param in continuous_parameters:
            call_col, left_col, right_col = param
            bins = sorted(data[left_col].unique())
            max_right = data[right_col].max()
            self.parameter_bins[(call_col, left_col, right_col)] = {
                "bins": bins,
                "max": max_right
            }

            if validate:
                # Check that left and right edges are consistent
                for _, row in data.iterrows():
                    assert row[left_col] <= row[right_col], f"Invalid bin edges for {param}"

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        '''Find the bins for each parameter for each interpolant in interpolants
        and return the values from data there.
        Parameters
        ----------
        interpolants
            Data frame containing the parameters to interpolate.
        Returns
        -------
            A table with the interpolated values for the given interpolants.
        '''
        result = pd.DataFrame(index=interpolants.index)
        merged = interpolants.copy()

        for (call_col, left_col, right_col), bin_info in self.parameter_bins.items():
            bins = bin_info["bins"]
            max_right = bin_info["max"]

            # Find the bin for each interpolant
            merged['_bin_index'] = pd.cut(
                merged[call_col],
                bins=bins +
                [max_right] if not self.extrapolate else bins + [float('inf')],
                labels=False,
                right=False
            )

            # Handle values outside bins (extrapolate or clamp)
            if not self.extrapolate:
                merged['_bin_index'] = merged['_bin_index'].clip(
                    lower=0, upper=len(bins)-1)

            # Merge with original data to get the values
            merged = merged.merge(
                self.data[[left_col] + self.value_columns],
                left_on='_bin_index',
                right_on=self.data[left_col].apply(lambda x: bins.index(x)),
                how='left'
            )

        result[self.value_columns] = merged[self.value_columns]
        return result
