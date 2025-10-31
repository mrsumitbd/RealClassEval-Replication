
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
                column_name = param[0]
                self.parameter_bins[(column_name, column_name, column_name)] = {
                    "bins": data[column_name].unique(),
                    "max": data[column_name].max()
                }
            elif len(param) == 3:
                call_column, left_column, right_column = param
                bins = data[left_column].unique()
                bins.sort()
                self.parameter_bins[(call_column, left_column, right_column)] = {
                    "bins": bins,
                    "max": data[right_column].max()
                }
            else:
                raise ValueError("Invalid continuous parameter specification")

        if validate:
            self._validate_data()

    def _validate_data(self):
        for (call_column, left_column, right_column), bins_dict in self.parameter_bins.items():
            bins = bins_dict["bins"]
            if not (bins[:-1] <= bins[1:]).all():
                raise ValueError(f"Bins for {call_column} are not sorted")

            data = self.data
            if not ((data[left_column] <= data[call_column]) & (data[call_column] < data[right_column])).all():
                raise ValueError(f"Data for {call_column} is not within bins")

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

        for index, interpolant in interpolants.iterrows():
            conditions = []
            for (call_column, left_column, right_column), bins_dict in self.parameter_bins.items():
                bins = bins_dict["bins"]
                max_value = bins_dict["max"]
                value = interpolant[call_column]

                if not self.extrapolate:
                    if value < bins[0] or value >= max_value:
                        raise ValueError(
                            f"Value {value} for {call_column} is out of range")

                idx = bins.searchsorted(value, side='right') - 1
                if idx < 0:
                    idx = 0
                elif idx >= len(bins):
                    idx = len(bins) - 1

                conditions.append(f"{left_column} == {bins[idx]}")

            condition = " & ".join(conditions)
            match = self.data.query(condition)

            if len(match) > 0:
                result.loc[index] = match[self.value_columns].iloc[0]
            else:
                result.loc[index] = float('nan')

        return result
