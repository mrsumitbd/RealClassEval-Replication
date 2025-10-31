
import pandas as pd
import numpy as np
from typing import Sequence, List


class Order0Interp:
    """
    Zero‑order (nearest‑neighbour) interpolation for tabular data.

    Parameters
    ----------
    data : pd.DataFrame
        Reference data containing the continuous parameters and the values to interpolate.
    continuous_parameters : Sequence[Sequence[str]]
        A sequence of sequences of column names that are treated as continuous parameters.
        All inner sequences are flattened and used to compute distances.
    value_columns : list[str]
        Column names in ``data`` whose values will be returned for each interpolant.
    extrapolate : bool
        If ``False`` an error is raised when an interpolant lies outside the bounds of
        the reference data. If ``True`` the nearest neighbour is returned regardless
        of bounds.
    validate : bool
        If ``True`` basic validation of column names is performed.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        continuous_parameters: Sequence[Sequence[str]],
        value_columns: List[str],
        extrapolate: bool,
        validate: bool,
    ):
        self.data = data.reset_index(drop=True)
        # Flatten continuous parameters
        self.continuous_params = [
            param for group in continuous_parameters for param in group
        ]
        self.value_columns = value_columns
        self.extrapolate = extrapolate
        self.validate = validate

        if self.validate:
            missing_in_data = set(self.continuous_params + self.value_columns) - set(
                self.data.columns
            )
            if missing_in_data:
                raise ValueError(
                    f"Columns missing in data: {sorted(missing_in_data)}"
                )

        # Pre‑compute bounds for extrapolation check
        self._bounds_min = self.data[self.continuous_params].min()
        self._bounds_max = self.data[self.continuous_params].max()

        # Convert data to numpy for fast distance calculation
        self._data_np = self.data[self.continuous_params].to_numpy()

    def __call__(self, interpolants: pd.DataFrame) -> pd.DataFrame:
        """
        Interpolate the values for the given interpolants.

        Parameters
        ----------
        interpolants : pd.DataFrame
            DataFrame containing the continuous parameters for which values are requested.

        Returns
        -------
        pd.DataFrame
            DataFrame with the same index as ``interpolants`` and columns ``value_columns``.
        """
        if self.validate:
            missing_in_interp = set(
                self.continuous_params) - set(interpolants.columns)
            if missing_in_interp:
                raise ValueError(
                    f"Interpolants missing required columns: {sorted(missing_in_interp)}"
                )

        # Convert interpolants to numpy
        interp_np = interpolants[self.continuous_params].to_numpy()

        # Check bounds if extrapolation not allowed
        if not self.extrapolate:
            out_of_bounds = (
                (interp_np < self._bounds_min.to_numpy()) | (
                    interp_np > self._bounds_max.to_numpy())
            )
            if out_of_bounds.any():
                idx = np.where(out_of_bounds.any(axis=1))[0]
                raise ValueError(
                    f"Interpolants at indices {idx.tolist()} are outside the bounds of the data."
                )

        # Compute distances (Euclidean)
        # Using broadcasting: (n_interp, 1, d) - (1, n_data, d)
        diff = interp_np[:, np.newaxis, :] - self._data_np[np.newaxis, :, :]
        dists = np.linalg.norm(diff, axis=2)  # shape (n_interp, n_data)

        # Find nearest neighbour indices
        nearest_idx = np.argmin(dists, axis=1)

        # Gather values
        result = self.data.iloc[nearest_idx][self.value_columns].reset_index(
            drop=True)

        # Preserve original index of interpolants
        result.index = interpolants.index
        return result
