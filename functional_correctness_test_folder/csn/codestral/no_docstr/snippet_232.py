
import pandas as pd
from typing import Sequence


class Order0Interp:

    def __init__(self, data: pd.DataFrame, continuous_parameters: Sequence[Sequence[str]], value_columns: list[str], extrapolate: bool, validate: bool):

        self.data = data
        self.continuous_parameters = continuous_parameters
        self.value_columns = value_columns
        self.extrapolate = extrapolate
        self.validate = validate

        if validate:
            self._validate_data()

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:

        if self.validate:
            self._validate_interpolants(interpolants)

        interpolated_values = []

        for _, row in interpolants.iterrows():
            interpolated_row = self._interpolate_row(row)
            interpolated_values.append(interpolated_row)

        return pd.DataFrame(interpolated_values)

    def _validate_data(self):

        for param_group in self.continuous_parameters:
            for param in param_group:
                if param not in self.data.columns:
                    raise ValueError(
                        f"Parameter {param} not found in data columns")

        for value_col in self.value_columns:
            if value_col not in self.data.columns:
                raise ValueError(
                    f"Value column {value_col} not found in data columns")

    def _validate_interpolants(self, interpolants: pd.DataFrame):

        for param_group in self.continuous_parameters:
            for param in param_group:
                if param not in interpolants.columns:
                    raise ValueError(
                        f"Parameter {param} not found in interpolants columns")

    def _interpolate_row(self, row: pd.Series) -> pd.Series:

        interpolated_row = pd.Series(index=self.value_columns)

        for value_col in self.value_columns:
            interpolated_row[value_col] = self._interpolate_value(
                row, value_col)

        return interpolated_row

    def _interpolate_value(self, row: pd.Series, value_col: str) -> float:

        distances = []

        for _, data_row in self.data.iterrows():
            distance = self._calculate_distance(row, data_row)
            distances.append((distance, data_row[value_col]))

        distances.sort(key=lambda x: x[0])

        if not self.extrapolate and distances[0][0] > 0:
            raise ValueError("Extrapolation not allowed")

        return distances[0][1]

    def _calculate_distance(self, row: pd.Series, data_row: pd.Series) -> float:

        distance = 0.0

        for param_group in self.continuous_parameters:
            group_distance = 0.0
            for param in param_group:
                group_distance += (row[param] - data_row[param]) ** 2
            distance += group_distance ** 0.5

        return distance
