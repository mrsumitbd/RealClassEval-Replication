
import pandas as pd
import numpy as np
from bisect import bisect_right
from collections.abc import Sequence
from typing import Dict, Tuple, List, Any


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
        A dictionary where the keys are a tuple of the form
        (column name used in call, column name for left bin edge, column name for right bin edge)
        and the values are dictionaries of the form {"bins": [ordered left edges of bins],
        "max": max right edge (used when extrapolation not allowed)}.
    '''

    def __init__(self, data: pd.DataFrame, continuous_parameters: Sequence[Sequence[str]],
                 value_columns: List[str], extrapolate: bool, validate: bool):
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
        self.parameter_bins: Dict[Tuple[str, str, str], Dict[str, Any]] = {}

        # Normalize continuous_parameters to tuples
        self.params: List[Tuple[str, str, str]] = []
        for p in continuous_parameters:
            if isinstance(p, str):
                # Assume column name used in call and left/right edges are same name with suffixes
                left_col = f"{p}_left"
                right_col = f"{p}_right"
                call_col = p
            else:
                call_col, left_col, right_col = p
            self.params.append((call_col, left_col, right_col))

        # Build parameter_bins
        for call_col, left_col, right_col in self.params:
            if left_col not in self.data.columns or right_col not in self.data.columns:
                raise ValueError(
                    f"Missing left/right columns for parameter {call_col}")
            left_edges = np.sort(self.data[left_col].unique())
            max_right = self.data[right_col].max()
            self.parameter_bins[(call_col, left_col, right_col)] = {
                "bins": left_edges,
                "max": max_right,
                "min": left_edges[0] if len(left_edges) > 0 else None
            }

        if validate:
            self._validate()

    def _validate(self):
        # Basic validation: left < right for all rows
        for _, row in self.data.iterrows():
            for _, left_col, right_col in self.params:
                if row[left_col] >= row[right_col]:
                    raise ValueError(
                        f"Invalid bin: left >= right in row {row.name}")

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
        # Prepare result DataFrame
        result = pd.DataFrame(index=interpolants.index,
                              columns=self.value_columns, dtype=float)

        # For each row in interpolants
        for idx, row in interpolants.iterrows():
            mask = pd.Series(True, index=self.data.index)

            for call_col, left_col, right_col in self.params:
                val = row[call_col]
                left_edges = self.parameter_bins[(
                    call_col, left_col, right_col)]["bins"]
                max_right = self.parameter_bins[(
                    call_col, left_col, right_col)]["max"]
                min_left = self.parameter_bins[(
                    call_col, left_col, right_col)]["min"]

                # Determine mask for this parameter
                if self.extrapolate:
                    # If outside bounds, use nearest bin
                    if val < min_left:
                        param_mask = self.data[left_col] == min_left
                    elif val >= max_right:
                        param_mask = self.data[left_col] == left_edges[-1]
                    else:
                        param_mask = (self.data[left_col] <= val) & (
                            self.data[right_col] > val)
                else:
                    # No extrapolation: require within bounds
                    param_mask = (self.data[left_col] <= val) & (
                        self.data[right_col] > val)

                mask &= param_mask

                # Early exit if no rows match
                if not mask.any():
                    break

            # If any row matches, take the first
            if mask.any():
                matched_row = self.data.loc[mask].iloc[0]
                result.loc[idx, self.value_columns] = matched_row[self.value_columns].values
            else:
                # No match: leave NaN
                result.loc[idx, self.value_columns] = np.nan

        return result
