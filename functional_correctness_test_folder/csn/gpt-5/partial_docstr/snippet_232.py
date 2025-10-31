import pandas as pd
import numpy as np
from typing import Sequence, Tuple, Dict, Any


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
        self.data = data.copy()
        self.value_columns = list(value_columns)
        self.extrapolate = bool(extrapolate)
        self.parameter_bins: Dict[Tuple[str, str, str], Dict[str, Any]] = {}

        for col in self.value_columns:
            if col not in self.data.columns:
                raise ValueError(f"value column {col} not found in data")

        for triple in continuous_parameters:
            if len(triple) != 3:
                raise ValueError(
                    "Each continuous parameter must be a sequence of three strings: (call_name, left_edge_col, right_edge_col)")
            call_name, left_col, right_col = triple
            if left_col not in self.data.columns or right_col not in self.data.columns:
                raise ValueError(
                    f"Bin edge columns {left_col} or {right_col} not found in data")

            unique_bins = self.data[[left_col, right_col]].drop_duplicates(
            ).sort_values([left_col, right_col], kind="mergesort")
            # Keep only the minimal right for each left in case of duplicates
            unique_bins = unique_bins.groupby(left_col, as_index=False)[
                right_col].min().sort_values(left_col, kind="mergesort")

            lefts = unique_bins[left_col].to_numpy()
            rights = unique_bins[right_col].to_numpy()

            if validate:
                if not np.all(np.isfinite(lefts)) or not np.all(np.isfinite(rights)):
                    raise ValueError(
                        f"Non-finite bin edges detected for parameter {call_name}")
                if not np.all(lefts[:-1] <= lefts[1:]):
                    raise ValueError(
                        f"Left edges must be non-decreasing for parameter {call_name}")
                if not np.all(rights > lefts):
                    raise ValueError(
                        f"Right edge must be greater than left edge for each bin of parameter {call_name}")
                # Ensure non-overlapping and sorted: lefts should be strictly increasing or equal to previous right
                if len(lefts) > 1:
                    if not np.all(lefts[1:] >= rights[:-1]):
                        raise ValueError(
                            f"Bins must be non-overlapping and ordered for parameter {call_name}")

            bins_sorted = list(
                map(lambda x: x.item() if hasattr(x, "item") else x, lefts))
            max_right = rights.max() if len(rights) else None
            if max_right is None:
                raise ValueError(
                    f"No bins available for parameter {call_name}")

            self.parameter_bins[(call_name, left_col, right_col)] = {
                "bins": bins_sorted, "max": max_right}

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        work = interpolants.copy()
        order_col = "_order__"
        while order_col in work.columns or order_col in self.data.columns:
            order_col += "_"
        work[order_col] = np.arange(len(work), dtype=np.int64)

        merge_keys = []
        for (call_name, left_col, right_col), meta in self.parameter_bins.items():
            if call_name not in work.columns:
                raise ValueError(
                    f"Interpolants missing required column {call_name}")
            values = work[call_name].to_numpy()
            bins = np.array(meta["bins"])
            max_right = meta["max"]

            # Find bin index using right-open intervals [left, right)
            idx = np.searchsorted(bins, values, side="right") - 1

            if self.extrapolate:
                idx = np.clip(idx, 0, len(bins) - 1)
            else:
                if len(bins) == 0:
                    raise ValueError("No bins available")
                too_low = values < bins[0]
                too_high = values >= max_right
                if np.any(too_low) or np.any(too_high):
                    raise ValueError(
                        f"Value(s) for {call_name} outside bin range and extrapolation is disabled")

            idx = np.clip(idx, 0, len(bins) - 1)
            chosen_lefts = bins[idx]

            # Determine matching right edges from data by left edge
            left_to_right = (
                self.data[[left_col, right_col]]
                .drop_duplicates()
                .sort_values([left_col, right_col], kind="mergesort")
                .groupby(left_col, as_index=True)[right_col]
                .min()
            )
            chosen_rights = left_to_right.reindex(chosen_lefts).to_numpy()

            work[left_col] = chosen_lefts
            work[right_col] = chosen_rights
            merge_keys.extend([left_col, right_col])

        # Perform merge
        cols_needed = list(dict.fromkeys(merge_keys + self.value_columns))
        merged = work.merge(self.data[cols_needed],
                            on=merge_keys, how="left", sort=False)

        merged = merged.sort_values(order_col, kind="mergesort")
        result = merged[self.value_columns].reset_index(drop=True)
        return result
