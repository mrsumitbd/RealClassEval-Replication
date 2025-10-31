import numpy as np
import pandas as pd
from collections.abc import Hashable, Sequence

class Order0Interp:
    """A callable that returns the result of order 0 interpolation over input data.

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

    """

    def __init__(self, data: pd.DataFrame, continuous_parameters: Sequence[Sequence[str]], value_columns: list[str], extrapolate: bool, validate: bool):
        """
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
        """
        if validate:
            check_data_complete(data, continuous_parameters)
        self.data = data.copy()
        self.value_columns = value_columns
        self.extrapolate = extrapolate
        self.parameter_bins = {}
        for p in continuous_parameters:
            left_edge = self.data[p[1]].drop_duplicates().sort_values()
            max_right = self.data[p[2]].drop_duplicates().max()
            self.parameter_bins[tuple(p)] = {'bins': left_edge.reset_index(drop=True), 'max': max_right}

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        """Find the bins for each parameter for each interpolant in interpolants
        and return the values from data there.

        Parameters
        ----------
        interpolants
            Data frame containing the parameters to interpolate..

        Returns
        -------
            A table with the interpolated values for the given interpolants.
        """
        interpolant_bins = pd.DataFrame(index=interpolants.index)
        merge_cols = []
        for cols, d in self.parameter_bins.items():
            bins = d['bins']
            max_right = d['max']
            merge_cols.append(cols[1])
            interpolant_col = interpolants[cols[0]]
            if not self.extrapolate and (interpolant_col.min() < bins[0] or interpolant_col.max() >= max_right):
                raise ValueError(f'Extrapolation outside of bins used to set up interpolation is only allowed when explicitly set in creation of Interpolation. Extrapolation is currently off for this interpolation, and parameter {cols[0]} includes data outside of original bins.')
            bin_indices = np.digitize(interpolant_col, bins.tolist())
            bin_indices[bin_indices > 0] -= 1
            interpolant_bins[cols[1]] = bins.loc[bin_indices].values
        index = interpolant_bins.index
        interp_vals = interpolant_bins.merge(self.data, how='left', on=merge_cols).set_index(index)
        return interp_vals[self.value_columns]