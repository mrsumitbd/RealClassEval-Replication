
import pandas as pd
from typing import Sequence


class Order0Interp:

    def __init__(self, data: pd.DataFrame, continuous_parameters: Sequence[Sequence[str]], value_columns: list[str], extrapolate: bool, validate: bool):
        self.data = data
        self.continuous_parameters = continuous_parameters
        self.value_columns = value_columns
        self.extrapolate = extrapolate
        self.validate = validate

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        results = pd.DataFrame(index=interpolants.index,
                               columns=self.value_columns)
        for idx, row in interpolants.iterrows():
            closest_row = self.data
            for params in self.continuous_parameters:
                for param in params:
                    closest_row = closest_row.iloc[(
                        closest_row[param] - row[param]).abs().argsort()[:1]]
            results.loc[idx] = closest_row[self.value_columns].iloc[0]
        return results
