
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
            if len(param) == 1:
                param = (param[0], param[0], param[0])
            call_col, left_col, right_col = param
            bins = sorted(data[left_col].unique())
            max_val = data[right_col].max()
            self.parameter_bins[call_col] = {"bins": bins, "max": max_val}

        if validate:
            self._validate_data()

    def _validate_data(self):
        for call_col, bin_info in self.parameter_bins.items():
            bins = bin_info["bins"]
            max_val = bin_info["max"]
            if not all(bins[i] <= bins[i+1] for i in range(len(bins)-1)):
                raise ValueError(f"Bins for {call_col} are not sorted.")
            if not all((self.data[call_col] >= bins[0]) & (self.data[call_col] < max_val)):
                raise ValueError(
                    f"Data for {call_col} is outside the provided bins.")

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
        result = pd.DataFrame(index=interpolants.index)

        for call_col, bin_info in self.parameter_bins.items():
            bins = bin_info["bins"]
            max_val = bin_info["max"]
            interpolant_values = interpolants[call_col]

            if not self.extrapolate:
                interpolant_values = interpolant_values.clip(
                    lower=bins[0], upper=max_val)

            bin_indices = pd.cut(interpolant_values,
                                 bins=bins, labels=False, right=False)
            result[call_col] = bin_indices

        for value_col in self.value_columns:
            result[value_col] = self.data[value_col].values[result.index]

        return result
