import pandas as pd
import numpy as np
from collections.abc import Hashable, Sequence

class Interpolation:
    """A callable that returns the result of an interpolation function over input data.

    Attributes
    ----------
    data :
        The data from which to build the interpolation. Contains
        categorical_parameters and continuous_parameters.
    categorical_parameters :
        Column names to be used as categorical parameters in Interpolation
        to select between interpolation functions.
    continuous_parameters :
        Column names to be used as continuous parameters in Interpolation. If
        bin edges, should be of the form (column name used in call, column name
        for left bin edge, column name for right bin edge).
    order :
        Order of interpolation.

    """

    def __init__(self, data: pd.DataFrame, categorical_parameters: Sequence[str], continuous_parameters: Sequence[Sequence[str]], value_columns: Sequence[str], order: int, extrapolate: bool, validate: bool):
        if order != 0:
            raise NotImplementedError(f'Interpolation is only supported for order 0. You specified order {order}')
        if validate:
            validate_parameters(data, categorical_parameters, continuous_parameters, value_columns)
        self.categorical_parameters = categorical_parameters
        self.data = data.copy()
        self.continuous_parameters = continuous_parameters
        self.value_columns = list(value_columns)
        self.order = order
        self.extrapolate = extrapolate
        self.validate = validate
        sub_tables: _SubTablesType
        if self.categorical_parameters:
            sub_tables = list(self.data.groupby(list(self.categorical_parameters)))
        else:
            sub_tables = [(None, self.data)]
        self.interpolations = {}
        for key, base_table in sub_tables:
            if base_table.empty:
                continue
            self.interpolations[key] = Order0Interp(base_table, self.continuous_parameters, self.value_columns, self.extrapolate, self.validate)

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        """Get the interpolated results for the parameters in interpolants.

        Parameters
         ----------
        interpolants :
            Data frame containing the parameters to interpolate..

        Returns
        -------
            A table with the interpolated values for the given interpolants.
        """
        if self.validate:
            validate_call_data(interpolants, self.categorical_parameters, self.continuous_parameters)
        sub_tables: _SubTablesType
        if self.categorical_parameters:
            sub_tables = list(interpolants.groupby(list(self.categorical_parameters), observed=False))
        else:
            sub_tables = [(None, interpolants)]
        result = pd.DataFrame(index=interpolants.index, columns=self.value_columns, dtype=np.float64)
        for key, sub_table in sub_tables:
            if sub_table.empty:
                continue
            df = self.interpolations[key](sub_table)
            result.loc[sub_table.index, list(self.value_columns)] = df.loc[sub_table.index, list(self.value_columns)]
        return result

    def __repr__(self) -> str:
        return 'Interpolation()'