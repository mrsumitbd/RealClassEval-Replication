
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
        self.data = data.copy()
        self.value_columns = value_columns
        self.extrapolate = extrapolate
        self.parameter_bins: Dict[Tuple[str, str, str], Dict] = {}

        for param in continuous_parameters:
            if isinstance(param, str):
                param_key = (param, param, param)
                left_col = param
                right_col = param
            else:
                param_key = tuple(param)
                left_col = param[1]
                right_col = param[2]

            bins = sorted(self.data[left_col].unique())
            max_right = self.data[right_col].max()
            self.parameter_bins[param_key] = {"bins": bins, "max": max_right}

        if validate:
            self._validate_data()

    def _validate_data(self):
        for param_key, bin_info in self.parameter_bins.items():
            left_col = param_key[1]
            right_col = param_key[2]
            bins = bin_info["bins"]
            for i in range(len(bins) - 1):
                left = bins[i]
                right = bins[i + 1]
                mask = (self.data[left_col] == left)
                if not all(self.data.loc[mask, right_col] == right):
                    raise ValueError(
                        f"Data validation failed for parameter {param_key}: inconsistent bin edges.")

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
        merged_data = self.data.copy()

        for param_key, bin_info in self.parameter_bins.items():
            call_col = param_key[0]
            left_col = param_key[1]
            right_col = param_key[2]
            bins = bin_info["bins"]
            max_right = bin_info["max"]

            values = interpolants[call_col].values
            if not self.extrapolate:
                if any((values < bins[0]) | (values > max_right)):
                    raise ValueError(
                        "Extrapolation not allowed and values outside bins provided.")

            bin_indices = pd.cut(
                values, bins=bins, labels=False, right=False, include_lowest=True)
            bin_indices = [len(bins) - 2 if pd.isna(i) or i >=
                           len(bins) - 1 else i for i in bin_indices]
            bin_values = [bins[i] for i in bin_indices]

            merged_data = merged_data.merge(
                pd.DataFrame(
                    {left_col: bin_values, '_tmp_index': range(len(bin_values))}),
                on=left_col,
                how='right'
            )
            merged_data = merged_data.sort_values('_tmp_index').drop_duplicates(
                subset=['_tmp_index'], keep='first')
            merged_data = merged_data.drop(columns=['_tmp_index'])

        for col in self.value_columns:
            result[col] = merged_data[col].values

        return result
