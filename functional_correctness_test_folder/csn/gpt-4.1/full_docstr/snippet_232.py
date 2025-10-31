
import pandas as pd
import numpy as np
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
        self.data = data.copy()
        self.value_columns = value_columns
        self.extrapolate = extrapolate
        self.parameter_bins = {}

        # Normalize continuous_parameters to tuples of (call_name, left_edge, right_edge)
        self.parameters = []
        for param in continuous_parameters:
            if isinstance(param, str):
                # Assume param is the column name, and bin edges are in that column
                self.parameters.append((param, param, param))
            else:
                self.parameters.append(tuple(param))

        for param in self.parameters:
            call_name, left_col, right_col = param
            # Get unique, sorted left edges
            bins = np.sort(self.data[left_col].unique())
            # Find the max right edge
            max_right = self.data[right_col].max()
            self.parameter_bins[param] = {
                "bins": bins,
                "max": max_right
            }

        if validate:
            # Check that bins are non-overlapping and sorted
            for param in self.parameters:
                left_col = param[1]
                right_col = param[2]
                df = self.data[[left_col, right_col]].sort_values(left_col)
                if not (df[left_col] < df[right_col]).all():
                    raise ValueError(
                        f"Left bin edge not less than right bin edge for parameter {param}")
                if not (df[right_col].shift(1).fillna(df[left_col].min()) <= df[left_col]).all():
                    raise ValueError(
                        f"Bins overlap or are not sorted for parameter {param}")

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
        # For each interpolant, find the row in self.data whose bins contain the interpolant value for each parameter
        # Build a mask for each parameter, then combine masks

        # Start with all True mask
        mask = pd.Series([True] * len(self.data), index=self.data.index)

        # For each interpolant row, find the matching data row
        results = []
        for idx, row in interpolants.iterrows():
            row_mask = pd.Series([True] * len(self.data),
                                 index=self.data.index)
            for param in self.parameters:
                call_name, left_col, right_col = param
                value = row[call_name]
                left_edges = self.data[left_col]
                right_edges = self.data[right_col]
                # Bin: left <= value < right
                param_mask = (left_edges <= value) & (value < right_edges)
                if not param_mask.any():
                    if self.extrapolate:
                        # If value < min(left_edges), use first bin
                        if value < left_edges.min():
                            param_mask = (left_edges == left_edges.min())
                        # If value >= max(right_edges), use last bin
                        elif value >= right_edges.max():
                            param_mask = (right_edges == right_edges.max())
                        else:
                            # Should not happen if bins are contiguous
                            raise ValueError(
                                f"Could not extrapolate for value {value} in parameter {call_name}")
                    else:
                        # No valid bin, return NaN for this row
                        param_mask = pd.Series(
                            [False] * len(self.data), index=self.data.index)
                row_mask &= param_mask
            # There should be exactly one row matching
            if row_mask.sum() == 1:
                data_row = self.data.loc[row_mask].iloc[0]
                result = {col: data_row[col] for col in self.value_columns}
            else:
                # No match or multiple matches, fill with NaN
                result = {col: np.nan for col in self.value_columns}
            results.append(result)
        return pd.DataFrame(results, index=interpolants.index)
