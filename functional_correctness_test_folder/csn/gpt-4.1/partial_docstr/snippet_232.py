
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
        self.data = data.copy()
        self.value_columns = value_columns
        self.extrapolate = extrapolate
        self.parameter_bins = {}

        # continuous_parameters: list of [call_col, left_col, right_col]
        for param in continuous_parameters:
            call_col, left_col, right_col = param
            # Get unique left edges, sorted
            bins = np.sort(self.data[left_col].unique())
            # Get max right edge
            max_right = self.data[right_col].max()
            self.parameter_bins[(call_col, left_col, right_col)] = {
                "bins": bins,
                "max": max_right
            }

        if validate:
            # Check that bins are non-overlapping and cover all data
            for (call_col, left_col, right_col), info in self.parameter_bins.items():
                bins = info["bins"]
                # For each bin, check that left < right
                for left in bins:
                    right = self.data.loc[self.data[left_col]
                                          == left, right_col].iloc[0]
                    if not left < right:
                        raise ValueError(
                            f"Bin left edge {left} not less than right edge {right} for {call_col}")
                # Check for overlapping bins
                right_edges = [self.data.loc[self.data[left_col]
                                             == left, right_col].iloc[0] for left in bins]
                for i in range(1, len(bins)):
                    if bins[i] < right_edges[i-1]:
                        raise ValueError(
                            f"Bins overlap for {call_col}: {bins[i]} < {right_edges[i-1]}")

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        '''Find the bins for each parameter for each interpolant in interpolants
        and return the values from data there.
        '''
        # For each interpolant, find the row in self.data that matches all bins
        # Build a mask for each interpolant
        results = []
        for idx, row in interpolants.iterrows():
            mask = pd.Series([True] * len(self.data))
            for (call_col, left_col, right_col), info in self.parameter_bins.items():
                x = row[call_col]
                bins = info["bins"]
                max_right = info["max"]
                # Find the bin: left <= x < right
                # If extrapolate, allow x < bins[0] or x >= max_right
                if self.extrapolate:
                    # Find the last bin where left <= x
                    left_idx = np.searchsorted(bins, x, side='right') - 1
                    if left_idx < 0:
                        left_idx = 0
                    left_edge = bins[left_idx]
                    right_edge = self.data.loc[self.data[left_col]
                                               == left_edge, right_col].iloc[0]
                else:
                    # Only allow x in [bins[0], max_right)
                    if x < bins[0] or x >= max_right:
                        raise ValueError(
                            f"Value {x} for {call_col} is out of bounds and extrapolate is False")
                    left_idx = np.searchsorted(bins, x, side='right') - 1
                    left_edge = bins[left_idx]
                    right_edge = self.data.loc[self.data[left_col]
                                               == left_edge, right_col].iloc[0]
                    if not (left_edge <= x < right_edge):
                        raise ValueError(
                            f"Value {x} for {call_col} not in any bin")
                # Update mask
                mask = mask & (self.data[left_col] == left_edge) & (
                    self.data[right_col] == right_edge)
            # Now mask should select a single row
            sel = self.data.loc[mask]
            if sel.empty:
                raise ValueError(
                    "No matching bin found for interpolant: {}".format(row.to_dict()))
            # Take the first matching row (should be unique)
            result_row = sel.iloc[0][self.value_columns]
            results.append(result_row)
        return pd.DataFrame(results, columns=self.value_columns).reset_index(drop=True)
