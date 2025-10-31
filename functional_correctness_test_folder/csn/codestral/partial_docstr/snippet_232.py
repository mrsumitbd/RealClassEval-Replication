
import pandas as pd
from typing import Sequence


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
            param_name, left_bin, right_bin = param
            bins = sorted(data[left_bin].unique())
            max_bin = data[right_bin].max()
            self.parameter_bins[param_name] = {"bins": bins, "max": max_bin}

        if validate:
            for param in continuous_parameters:
                param_name, left_bin, right_bin = param
                for i in range(len(self.parameter_bins[param_name]["bins"]) - 1):
                    assert self.data[(self.data[left_bin] == self.parameter_bins[param_name]["bins"][i]) &
                                     (self.data[right_bin] == self.parameter_bins[param_name]["bins"][i+1])].shape[0] > 0, \
                        f"No data found for bin {self.parameter_bins[param_name]['bins'][i]} to {self.parameter_bins[param_name]['bins'][i+1]}"

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
        result = pd.DataFrame()
        for param_name, bins_info in self.parameter_bins.items():
            bins = bins_info["bins"]
            max_bin = bins_info["max"]

            interpolant_values = interpolants[param_name]
            bin_indices = pd.cut(interpolant_values,
                                 bins=bins, labels=False, right=False)

            if not self.extrapolate:
                bin_indices = bin_indices[interpolant_values <= max_bin]

            result[param_name] = bin_indices

        result = result.dropna()
        result = result.astype(int)

        interpolated_values = self.data.iloc[result.index]
        interpolated_values = interpolated_values[self.value_columns]

        return interpolated_values
