
import numpy as np
import matplotlib.pyplot as plt


class ModelGridPlotMixin:

    def _reshape_grid(self, data):
        if not isinstance(data, np.ndarray):
            raise ValueError("Data must be a numpy array.")
        if data.ndim != 2:
            raise ValueError("Data must be a 2D array.")
        return data

    def plot_grid(self, *, ax=None, vmax_scale=None, peak_norm=False, deltas=False, cmap='viridis', dividers=True, divider_color='darkgray', divider_ls='-', figsize=None):
        data = self._reshape_grid(self.data)

        if peak_norm:
            data = data / np.max(np.abs(data))

        if deltas:
            data = np.diff(data, axis=0)
            data = np.diff(data, axis=1)

        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure

        if vmax_scale is not None:
            vmax = np.max(np.abs(data)) * vmax_scale
        else:
            vmax = None

        im = ax.imshow(data, cmap=cmap, vmax=vmax,
                       vmin=-vmax if vmax else None)

        if dividers:
            for i in range(data.shape[0] + 1):
                ax.axhline(i - 0.5, color=divider_color, linestyle=divider_ls)
                ax.axvline(i - 0.5, color=divider_color, linestyle=divider_ls)

        fig.colorbar(im, ax=ax)
        plt.show()
