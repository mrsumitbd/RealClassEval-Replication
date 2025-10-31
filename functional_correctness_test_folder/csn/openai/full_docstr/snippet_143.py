
import numpy as np
import matplotlib.pyplot as plt


class ModelGridPlotMixin:
    """
    Mixin class to plot a grid of ePSF models.
    """

    def _reshape_grid(self, data):
        """
        Reshape the 3D ePSF grid as a 2D array of horizontally and
        vertically stacked ePSFs.
        Parameters
        ----------
        data : `numpy.ndarray`
            The 3D array of ePSF data.
        Returns
        -------
        reshaped_data : `numpy.ndarray`
            The 2D array of ePSF data.
        """
        # Determine grid shape
        if hasattr(self, "grid_shape"):
            n_rows, n_cols = self.grid_shape
        else:
            n_grid = data.shape[0]
            n_rows = n_cols = int(np.sqrt(n_grid))
        size = data.shape[1]
        # Reshape into 4D array: (n_rows, n_cols, size, size)
        grid = data.reshape(n_rows, n_cols, size, size)
        # Concatenate horizontally within each row
        rows = [np.concatenate([grid[i, j] for j in range(n_cols)], axis=1)
                for i in range(n_rows)]
        # Concatenate vertically
        reshaped = np.concatenate(rows, axis=0)
        return reshaped

    def plot_grid(
        self,
        *,
        ax=None,
        vmax_scale=None,
        peak_norm=False,
        deltas=False,
        cmap="viridis",
        dividers=True,
        divider_color="darkgray",
        divider_ls="-",
        figsize=None,
    ):
        """
        Plot the grid of ePSF models.
        Parameters
        ----------
        ax : `matplotlib
