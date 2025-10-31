import numpy as np
import pandas as pd
from typing import Sequence


class Order0Interp:

    def __init__(self, data: pd.DataFrame, continuous_parameters: Sequence[Sequence[str]], value_columns: list[str], extrapolate: bool, validate: bool):
        # Flatten and deduplicate parameter names in order
        flat_params: list[str] = []
        for group in continuous_parameters:
            for col in group:
                if col not in flat_params:
                    flat_params.append(col)
        self.param_cols = flat_params
        self.value_cols = list(value_columns)
        self.extrapolate = bool(extrapolate)

        # Basic validations
        missing_params = [c for c in self.param_cols if c not in data.columns]
        if missing_params:
            raise ValueError(
                f"Missing parameter columns in data: {missing_params}")
        missing_values = [c for c in self.value_cols if c not in data.columns]
        if missing_values:
            raise ValueError(
                f"Missing value columns in data: {missing_values}")
        if len(self.param_cols) == 0:
            raise ValueError("At least one parameter column is required.")

        df = data[self.param_cols + self.value_cols].copy()

        if validate:
            if df[self.param_cols].isna().any().any():
                raise ValueError("NaNs found in parameter columns.")
            if df[self.value_cols].isna().any().any():
                # Allow NaNs in values but warn by raising if strict validate
                raise ValueError("NaNs found in value columns.")

        # Aggregate duplicate parameter rows by averaging value columns
        if df.duplicated(subset=self.param_cols).any():
            df = df.groupby(self.param_cols, as_index=False, dropna=False)[
                self.value_cols].mean()

        # Cache arrays
        self._X = df[self.param_cols].to_numpy(dtype=float, copy=True)
        self._Y = df[self.value_cols].to_numpy(dtype=float, copy=True)

        # Bounds for extrapolation handling
        self._mins = np.nanmin(self._X, axis=0)
        self._maxs = np.nanmax(self._X, axis=0)

        # Precompute norms for distance calculations
        self._X_sq = np.einsum("ij,ij->i", self._X, self._X)

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(interpolants, pd.DataFrame):
            raise TypeError("interpolants must be a pandas DataFrame.")

        missing = [c for c in self.param_cols if c not in interpolants.columns]
        if missing:
            raise ValueError(
                f"Missing parameter columns in interpolants: {missing}")

        Q = interpolants[self.param_cols].to_numpy(dtype=float, copy=False)
        m = Q.shape[0]
        n = self._X.shape[0]

        # Identify out-of-bounds rows if not extrapolating
        if self.extrapolate:
            valid_mask = np.ones(m, dtype=bool)
        else:
            valid_mask = (Q >= self._mins).all(
                axis=1) & (Q <= self._maxs).all(axis=1)

        # Prepare output
        out = np.full((m, self._Y.shape[1]), np.nan, dtype=float)

        if n == 0 or m == 0:
            return pd.DataFrame(out, index=interpolants.index, columns=self.value_cols)

        # Chunked nearest neighbor search to limit memory
        # target elements in distance matrix ~ 1e7 (80MB for float64)
        target_elems = 10_000_000
        chunk = max(1, int(target_elems // max(1, n)))

        X = self._X
        X_sq = self._X_sq
        Y = self._Y

        idxs = np.arange(m)[valid_mask]
        for start in range(0, idxs.size, chunk):
            sl = idxs[start:start + chunk]
            Q_chunk = Q[sl]

            # Compute squared distances: ||q||^2 + ||x||^2 - 2 q.x
            Q_sq = np.einsum("ij,ij->i", Q_chunk, Q_chunk)
            # Q_chunk @ X.T shape (k, n)
            cross = Q_chunk @ X.T
            d2 = Q_sq[:, None] + X_sq[None, :] - 2.0 * cross

            nn_idx = np.argmin(d2, axis=1)
            out[sl] = Y[nn_idx]

        return pd.DataFrame(out, index=interpolants.index, columns=self.value_cols)
