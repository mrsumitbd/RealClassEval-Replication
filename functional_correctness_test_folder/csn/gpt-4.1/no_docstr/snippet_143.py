
import numpy as np
import matplotlib.pyplot as plt


class ModelGridPlotMixin:

    def _reshape_grid(self, data):
        """
        Reshape a 1D or 2D array into a 2D grid if possible.
        If data is already 2D, return as is.
        If data is 1D and a square, reshape to (n, n).
        Otherwise, raise ValueError.
        """
        arr = np.asarray(data)
        if arr.ndim == 2:
            return arr
        elif arr.ndim == 1:
            n = int(np.sqrt(arr.size))
            if n * n != arr.size:
                raise ValueError("Cannot reshape data to square grid.")
            return arr.reshape((n, n))
        else:
            raise ValueError("Data must be 1D or 2D array.")

    def plot_grid(self, *, ax=None, vmax_scale=None, peak_norm=False, deltas=False, cmap='viridis', dividers=True, divider_color='darkgray', divider_ls='-', figsize=None):
        """
        Plot a 2D grid of data with optional normalization, dividers, and color scaling.
        Assumes self.grid_data exists and is the data to plot.
        """
        # Get data
        data = getattr(self, 'grid_data', None)
        if data is None:
            raise AttributeError(
                "Instance must have 'grid_data' attribute to plot.")
        grid = self._reshape_grid(data)
        grid = np.array(grid, dtype=float)

        # Optionally plot deltas (differences between adjacent cells)
        if deltas:
            grid = np.diff(grid, axis=0)
            if grid.shape[0] == 0:
                raise ValueError("Not enough rows for deltas.")

        # Normalization
        if peak_norm:
            vmax = np.nanmax(np.abs(grid))
            vmin = -vmax
        else:
            vmin, vmax = np.nanmin(grid), np.nanmax(grid)

        if vmax_scale is not None:
            vmax = vmax_scale
            vmin = -vmax_scale if peak_norm else np.nanmin(grid)

        # Setup axis
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure

        # Plot
        im = ax.imshow(grid, cmap=cmap, vmin=vmin, vmax=vmax,
                       origin='upper', aspect='auto')

        # Add dividers
        if dividers:
            nrows, ncols = grid.shape
            for i in range(1, nrows):
                ax.axhline(i - 0.5, color=divider_color,
                           linestyle=divider_ls, linewidth=1)
            for j in range(1, ncols):
                ax.axvline(j - 0.5, color=divider_color,
                           linestyle=divider_ls, linewidth=1)

        # Colorbar
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        # Tidy up
        ax.set_xticks(np.arange(grid.shape[1]))
        ax.set_yticks(np.arange(grid.shape[0]))
        ax.set_xlim(-0.5, grid.shape[1] - 0.5)
        ax.set_ylim(grid.shape[0] - 0.5, -0.5)
        ax.set_aspect('equal')

        return ax
