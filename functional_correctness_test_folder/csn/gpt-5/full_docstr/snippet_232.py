import pandas as pd
import numpy as np
from typing import Sequence, Union, Tuple


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
        self.data = data.copy()
        self.value_columns = list(value_columns)
        self.extrapolate = bool(extrapolate)

        # Separate continuous (triplet) and discrete (single name) parameters
        cont_params: list[Tuple[str, str, str]] = []
        disc_params: list[str] = []

        for p in continuous_parameters:
            if isinstance(p, (list, tuple)):
                if len(p) == 3:
                    cont_params.append((p[0], p[1], p[2]))
                elif len(p) == 1:
                    disc_params.append(p[0])
                else:
                    raise ValueError(
                        "Each parameter must be either a single column name or a triplet (call_name, left_edge_col, right_edge_col).")
            elif isinstance(p, str):
                disc_params.append(p)
            else:
                raise ValueError(
                    "Parameter entries must be sequences of strings or a string.")

        # Build parameter_bins for continuous parameters
        self.parameter_bins: dict[tuple[str, str, str],
                                  dict[str, Union[list[float], float]]] = {}
        for call_name, left_col, right_col in cont_params:
            if left_col not in self.data.columns or right_col not in self.data.columns:
                raise KeyError(
                    f"Missing bin edge columns '{left_col}' or '{right_col}' in data for parameter '{call_name}'.")
            left_edges = np.sort(self.data[left_col].dropna().unique())
            max_right = float(np.nanmax(self.data[right_col].values))
            self.parameter_bins[(call_name, left_col, right_col)] = {
                "bins": left_edges.tolist(),
                "max": max_right,
            }

            if validate:
                if left_edges.size == 0:
                    raise ValueError(
                        f"No left bin edges found for parameter '{call_name}'.")
                if not np.all(np.diff(left_edges) > 0):
                    raise ValueError(
                        f"Left bin edges for parameter '{call_name}' must be strictly increasing.")
                if max_right <= left_edges[-1]:
                    raise ValueError(
                        f"Max right edge for parameter '{call_name}' must be greater than the last left edge.")
                # Ensure at least one row per left edge exists
                counts = self.data[left_col].value_counts()
                for v in left_edges:
                    if counts.get(v, 0) == 0:
                        raise ValueError(
                            f"No data rows for left edge {v} in parameter '{call_name}'.")

        # Store discrete parameters
        self.discrete_parameters: list[str] = []
        for c in disc_params:
            if c not in self.data.columns:
                raise KeyError(
                    f"Discrete parameter column '{c}' not found in data.")
            self.discrete_parameters.append(c)

        # Validate value columns
        missing_values = [
            c for c in self.value_columns if c not in self.data.columns]
        if missing_values:
            raise KeyError(
                f"Value columns not found in data: {missing_values}")

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
        if not isinstance(interpolants, pd.DataFrame):
            raise TypeError("interpolants must be a pandas DataFrame.")

        tmp = interpolants.copy()
        idx_name = tmp.index.name
        tmp = tmp.reset_index(drop=False).rename(columns={
            tmp.index.name or "index": "__row_id__"}) if idx_name is None else tmp.reset_index().rename(columns={idx_name: "__row_id__"})

        # Compute bin assignments for continuous parameters
        bin_assign_cols = {}
        for (call_name, left_col, right_col), meta in self.parameter_bins.items():
            if call_name not in tmp.columns:
                raise KeyError(
                    f"Interpolants missing required parameter '{call_name}'.")
            values = tmp[call_name].astype(float).to_numpy()
            bins = np.array(meta["bins"], dtype=float)
            max_right = float(meta["max"])

            # searchsorted returns insertion index to maintain order
            # For value in [bins[i], bins[i+1]) we want index i
            idxs = np.searchsorted(bins, values, side="right") - 1

            # Handle out-of-range
            low_mask = values < bins[0]
            high_mask = values >= max_right  # right edge exclusive
            if self.extrapolate:
                idxs = np.clip(idxs, 0, len(bins) - 1)
            else:
                idxs[low_mask] = -1
                # For values between last left edge and max_right, idx is valid
                # For values >= max_right, set to -1
                idxs[high_mask] = -1

            # Map to left edge values; -1 -> NaN
            left_assigned = np.where(
                idxs >= 0, bins[np.clip(idxs, 0, len(bins) - 1)], np.nan)
            assign_col = f"__bin__{left_col}"
            tmp[assign_col] = left_assigned
            bin_assign_cols[left_col] = assign_col

        # Prepare merge keys: continuous left edge columns and discrete columns
        merge_left = []
        merge_right = []
        for left_col, assign_col in bin_assign_cols.items():
            merge_left.append(assign_col)
            merge_right.append(left_col)

        for col in self.discrete_parameters:
            if col not in tmp.columns:
                raise KeyError(
                    f"Interpolants missing required discrete parameter '{col}'.")
            merge_left.append(col)
            merge_right.append(col)

        # If no parameters, just broadcast values
        if not merge_left:
            result = pd.DataFrame(self.data[self.value_columns].iloc[:1].values.repeat(
                len(tmp), axis=0), columns=self.value_columns)
            result["__row_id__"] = tmp["__row_id__"] if "__row_id__" in tmp.columns else np.arange(
                len(tmp))
        else:
            merged = tmp.merge(self.data[self.value_columns + merge_right],
                               left_on=merge_left, right_on=merge_right, how="left", copy=False)

            # Preserve row order
            result = merged[["__row_id__", *self.value_columns]].copy()

        # Restore original index order
        if "__row_id__" in interpolants.reset_index().columns:
            # Unlikely name collision; ensure unique mapping
            # We'll sort by position introduced earlier
            pass

        result = result.set_index("__row_id__").sort_index()
        # If original had a named index, keep it; else range
        return result[self.value_columns]
