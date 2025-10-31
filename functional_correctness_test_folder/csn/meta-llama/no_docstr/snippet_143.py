
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


class ModelGridPlotMixin:

    def _reshape_grid(self, data):
        """Reshape data into a grid format."""
        # Assuming data is a 1D array and self.grid_shape is a tuple representing the grid dimensions
        return np.reshape(data, self.grid_shape)

    def plot_grid(self, *, ax=None, vmax_scale=None, peak_norm=False, deltas=False, cmap='viridis', dividers=True, divider_color='darkgray', divider_ls='-', figsize=None):
        """Plot the grid data."""
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.get_figure()

        grid_data = self._reshape_grid(self.data)

        if deltas:
            grid_data = grid_data - np.mean(grid_data)

        if peak_norm:
            vmax = np.max(np.abs(grid_data))
            vmin = -vmax
        else:
            vmax = np.max(grid_data)
            vmin = np.min(grid_data)

        if vmax_scale is not None:
            vmax *= vmax_scale
            vmin = -vmax if peak_norm else vmin

        im = ax.imshow(grid_data, cmap=cmap, vmin=vmin,
                       vmax=vmax, origin='lower')

        if dividers:
            for i in range(1, self.grid_shape[0]):
                ax.axhline(i - 0.5, color=divider_color, ls=divider_ls)
            for i in range(1, self.grid_shape[1]):
                ax.axvline(i - 0.5, color=divider_color, ls=divider_ls)

        ax.set_xticks([])
        ax.set_yticks([])

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)

        return fig, ax
