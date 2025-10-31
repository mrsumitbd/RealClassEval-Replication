
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

    def _validate_data(self):
        if not all(col in self.data.columns for col in self.value_columns):
            raise ValueError("Some value_columns are not present in the data.")
        for param_group in self.continuous_parameters:
            if not all(param in self.data.columns for param in param_group):
                raise ValueError(
                    "Some continuous_parameters are not present in the data.")

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        result = interpolants.copy()

        for col in self.value_columns:
            result[col] = None

        for idx, row in interpolants.iterrows():
            for param_group in self.continuous_parameters:
                mask = None
                for param in param_group:
                    if mask is None:
                        mask = (self.data[param] <= row[param])
                    else:
                        mask &= (self.data[param] <= row[param])

                if not mask.any():
                    if self.extrapolate:
                        closest_idx = self._find_closest(row, param_group)
                        for col in self.value_columns:
                            result.at[idx, col] = self.data.at[closest_idx, col]
                    else:
                        for col in self.value_columns:
                            result.at[idx, col] = None
                else:
                    last_valid_idx = mask.idxmax()
                    for col in self.value_columns:
                        result.at[idx, col] = self.data.at[last_valid_idx, col]

        return result

    def _find_closest(self, row: pd.Series, param_group: Sequence[str]) -> int:
        distances = []
        for _, data_row in self.data.iterrows():
            distance = sum((row[param] - data_row[param])
                           ** 2 for param in param_group)
            distances.append(distance)
        return distances.index(min(distances))
