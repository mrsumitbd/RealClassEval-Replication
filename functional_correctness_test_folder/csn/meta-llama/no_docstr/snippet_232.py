
import pandas as pd
from typing import Sequence


class Order0Interp:

    def __init__(self, data: pd.DataFrame, continuous_parameters: Sequence[Sequence[str]], value_columns: list[str], extrapolate: bool, validate: bool):
        self.data = data
        self.continuous_parameters = continuous_parameters
        self.value_columns = value_columns
        self.extrapolate = extrapolate
        self.validate = validate

        # Validate input data
        if validate:
            self._validate_input()

        # Create a MultiIndex for efficient lookup
        self.data_multi_index = self.data.set_index(
            [param for params in continuous_parameters for param in params])

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        # Set index for interpolants DataFrame
        interpolants_multi_index = interpolants.set_index(
            [param for params in self.continuous_parameters for param in params])

        # Perform interpolation
        interpolated_values = self._interpolate(interpolants_multi_index)

        return interpolated_values.reset_index()

    def _validate_input(self):
        # Check if all value columns exist in data
        for col in self.value_columns:
            if col not in self.data.columns:
                raise ValueError(f"Value column '{col}' not found in data")

        # Check if all continuous parameters exist in data
        for params in self.continuous_parameters:
            for param in params:
                if param not in self.data.columns:
                    raise ValueError(
                        f"Continuous parameter '{param}' not found in data")

        # Check if interpolants DataFrame has the same continuous parameters
        # This check is performed in __call__ method

    def _interpolate(self, interpolants_multi_index: pd.DataFrame):
        interpolated_values = []

        for index, row in interpolants_multi_index.iterrows():
            try:
                # Find the nearest point in the data
                nearest_point = self._find_nearest_point(index)
                interpolated_row = self.data_multi_index.loc[nearest_point,
                                                             self.value_columns]
                interpolated_values.append(interpolated_row.values)
            except KeyError:
                if self.extrapolate:
                    # If extrapolation is allowed, use the nearest point
                    nearest_point = self._find_nearest_point(
                        index, extrapolate=True)
                    interpolated_row = self.data_multi_index.loc[nearest_point,
                                                                 self.value_columns]
                    interpolated_values.append(interpolated_row.values)
                else:
                    # If extrapolation is not allowed, raise an error or return NaN
                    interpolated_values.append(
                        [float('nan')] * len(self.value_columns))

        interpolated_df = pd.DataFrame(
            interpolated_values, index=interpolants_multi_index.index, columns=self.value_columns)

        return interpolated_df

    def _find_nearest_point(self, point, extrapolate=False):
        # Find the nearest point in the data
        idx = self.data_multi_index.index.get_indexer(
            [point], method='nearest')

        if not extrapolate and idx[0] == -1:
            raise KeyError(f"No nearest point found for {point}")

        nearest_point = self.data_multi_index.index[idx[0]]

        return nearest_point
