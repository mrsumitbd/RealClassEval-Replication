
import pandas as pd
import numpy as np
from typing import Sequence, List


class Order0Interp:

    def __init__(self, data: pd.DataFrame, continuous_parameters: Sequence[Sequence[str]], value_columns: list[str], extrapolate: bool, validate: bool):
        self.data = data.copy()
        self.continuous_parameters = [list(group)
                                      for group in continuous_parameters]
        self.value_columns = value_columns
        self.extrapolate = extrapolate
        self.validate = validate

        # Flatten all parameter names
        self.param_names = [
            p for group in self.continuous_parameters for p in group]

        # Validation
        if self.validate:
            for group in self.continuous_parameters:
                if not all(col in self.data.columns for col in group):
                    raise ValueError(
                        f"Some continuous parameter columns {group} not in data")
            for col in self.value_columns:
                if col not in self.data.columns:
                    raise ValueError(f"Value column {col} not in data")
            if self.data.duplicated(subset=self.param_names).any():
                raise ValueError("Duplicate parameter combinations in data")

        # Build a lookup index for fast matching
        self.data_indexed = self.data.set_index(self.param_names)

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        # Prepare result DataFrame
        result = interpolants.copy()
        # For each row in interpolants, find the closest (order 0) match in self.data
        matched_values = []
        for idx, row in interpolants.iterrows():
            # For each group, find the closest value in data
            key = []
            for group in self.continuous_parameters:
                # For each group, treat as a tuple if more than one parameter
                if len(group) == 1:
                    col = group[0]
                    val = row[col]
                    # Find closest value in data
                    candidates = self.data[col].unique()
                    diffs = np.abs(candidates - val)
                    min_idx = np.argmin(diffs)
                    closest = candidates[min_idx]
                    key.append(closest)
                else:
                    vals = tuple(row[col] for col in group)
                    candidates = self.data[list(
                        group)].drop_duplicates().values
                    diffs = np.linalg.norm(candidates - np.array(vals), axis=1)
                    min_idx = np.argmin(diffs)
                    closest = candidates[min_idx]
                    key.extend(closest)
            # Try to get the value from the indexed data
            try:
                value_row = self.data_indexed.loc[tuple(key)]
                matched_values.append(value_row[self.value_columns].values)
            except KeyError:
                if self.extrapolate:
                    # Clamp to nearest available value in data
                    clamped_key = []
                    for i, group in enumerate(self.continuous_parameters):
                        if len(group) == 1:
                            col = group[0]
                            val = row[col]
                            candidates = self.data[col].unique()
                            idx_closest = np.argmin(np.abs(candidates - val))
                            clamped_key.append(candidates[idx_closest])
                        else:
                            vals = tuple(row[col] for col in group)
                            candidates = self.data[list(
                                group)].drop_duplicates().values
                            idx_closest = np.argmin(np.linalg.norm(
                                candidates - np.array(vals), axis=1))
                            clamped_key.extend(candidates[idx_closest])
                    try:
                        value_row = self.data_indexed.loc[tuple(clamped_key)]
                        matched_values.append(
                            value_row[self.value_columns].values)
                    except KeyError:
                        matched_values.append(
                            [np.nan] * len(self.value_columns))
                else:
                    matched_values.append([np.nan] * len(self.value_columns))
        matched_values = np.array(matched_values)
        for i, col in enumerate(self.value_columns):
            result[col] = matched_values[:, i]
        return result
