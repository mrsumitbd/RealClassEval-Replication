
import pandas as pd
from typing import Sequence, Dict, Tuple, Any


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

    def __init__(self,
                 data: pd.DataFrame,
                 continuous_parameters: Sequence[Sequence[str]],
                 value_columns: list[str],
                 extrapolate: bool,
                 validate: bool = False):
        self.data = data
        self.value_columns = value_columns
        self.extrapolate = extrapolate

        # Build parameter_bins dictionary
        self.parameter_bins: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
        for param in continuous_parameters:
            if len(param) != 3:
                raise ValueError(
                    "Each continuous parameter must be a sequence of 3 strings")
            call_col, left_col, right_col = param
            left_edges = sorted(self.data[left_col].unique())
            max_right = self.data[right_col].max()
            self.parameter_bins[(call_col, left_col, right_col)] = {
                "bins": left_edges,
                "max": max_right
            }

        if validate:
            # Basic validation: ensure all required columns exist
            required_cols = set()
            for _, left_col, right_col in self.parameter_bins:
                required_cols.update([left_col, right_col])
            required_cols.update(self.value_columns)
            missing = required_cols - set(self.data.columns)
            if missing:
                raise ValueError(f"Missing columns in data: {missing}")

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
        # Prepare result DataFrame
        result = pd.DataFrame(index=interpolants.index,
                              columns=self.value_columns, dtype=float)

        # If no parameters, return NaNs
        if not self.parameter_bins:
            return result

        # Iterate over each row in interpolants
        for idx, row in interpolants.iterrows():
            mask = pd.Series(True, index=self.data.index)

            # Apply each parameter binning
            for (call_col, left_col, right_col), bin_info in self.parameter_bins.items():
                val = row.get(call_col, None)
                if pd.isna(val):
                    mask = pd.Series(False, index=self.data.index)
                    break

                # Extrapolation check
                if not self.extrapolate:
                    if val < bin_info["bins"][0] or val > bin_info["max"]:
                        mask = pd.Series(False, index=self.data.index)
                        break

                # Bin selection: left <= val < right
                mask &= (self.data[left_col] <= val) & (
                    val < self.data[right_col])

                if not mask.any():
                    break

            # If a matching row exists, take the first one
            if mask.any():
                matched_row = self.data.loc[mask].iloc[0]
                result.loc[idx, self.value_columns] = matched_row[self.value_columns].values
            else:
                # No match: leave NaNs
                continue

        return result
