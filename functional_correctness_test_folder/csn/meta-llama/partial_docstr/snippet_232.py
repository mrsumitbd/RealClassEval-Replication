
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

        for params in continuous_parameters:
            if len(params) != 3:
                raise ValueError(
                    "Continuous parameters must be a sequence of length 3")
            call_col, left_col, right_col = params

            bins = data[left_col].unique().tolist() + [data[right_col].max()]
            bins.sort()
            self.parameter_bins[(call_col, left_col, right_col)] = {
                "bins": bins, "max": bins[-1]}

            if validate:
                if not (data[left_col] <= data[right_col]).all():
                    raise ValueError(
                        f"Left bin edge ({left_col}) is not always less than or equal to right bin edge ({right_col})")
                if not (data[call_col] >= data[left_col]).all() or not (data[call_col] <= data[right_col]).all():
                    raise ValueError(
                        f"Interpolant ({call_col}) is not always within bin edges ({left_col}, {right_col})")

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
        result = pd.DataFrame(index=interpolants.index,
                              columns=self.value_columns)

        for _, row in interpolants.iterrows():
            idx = row.name
            for value_col in self.value_columns:
                interpolated_value = None
                for params, bins_dict in self.parameter_bins.items():
                    call_col, _, _ = params
                    if call_col in interpolants.columns:
                        bin_idx = None
                        bins = bins_dict["bins"]
                        max_bin = bins_dict["max"]
                        interpolant = row[call_col]

                        if interpolant < bins[0] and not self.extrapolate:
                            interpolated_value = float('nan')
                            break
                        elif interpolant >= max_bin and not self.extrapolate:
                            interpolated_value = float('nan')
                            break
                        else:
                            bin_idx = next((i for i, x in enumerate(
                                bins) if x > interpolant), len(bins) - 1) - 1
                            if bin_idx < 0:
                                bin_idx = 0
                            mask = True
                            for params, bins_dict in self.parameter_bins.items():
                                call_col, left_col, right_col = params
                                if call_col in interpolants.columns:
                                    bins = bins_dict["bins"]
                                    interpolant = row[call_col]
                                    bin_idx_param = next((i for i, x in enumerate(
                                        bins) if x > interpolant), len(bins) - 1) - 1
                                    if bin_idx_param < 0:
                                        bin_idx_param = 0
                                    mask &= (self.data[left_col] == bins[bin_idx_param]) & (
                                        self.data[right_col] == bins[bin_idx_param + 1])
                            if mask.any():
                                interpolated_value = self.data.loc[mask,
                                                                   value_col].iloc[0]
                            else:
                                interpolated_value = float('nan')
                                break
                result.loc[idx, value_col] = interpolated_value
        return result
