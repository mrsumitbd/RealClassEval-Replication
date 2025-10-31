
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class ModelGridPlotMixin:

    def _reshape_grid(self, data):
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        if data.ndim == 1:
            n = int(np.sqrt(len(data)))
            if n * n != len(data):
                raise ValueError(
                    "1D data length must be a perfect square for reshaping to a grid.")
            return data.reshape(n, n)
        elif data.ndim == 2:
            return data
        else:
            raise ValueError("Data must be 1D or 2D.")

    def plot_grid(self, *, ax=None, vmax_scale=None, peak_norm=False, deltas=False, cmap='viridis', dividers=True, divider_color='darkgray', divider_ls='-', figsize=None):
        data = self._get_data() if hasattr(self, '_get_data') else None
        if data is None:
            raise ValueError("No data available for plotting.")

        data = self._reshape_grid(data)

        if deltas:
            data = data - np.mean(data)

        if peak_norm:
            data = data / np.max(np.abs(data)
                                 ) if np.max(np.abs(data)) != 0 else data

        vmax = np.max(np.abs(data)) * \
            vmax_scale if vmax_scale is not None else None

        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)

        im = ax.imshow(data, cmap=cmap, vmin=-
                       vmax if vmax is not None else None, vmax=vmax)

        if dividers:
            n_rows, n_cols = data.shape
            for i in range(1, n_rows):
                ax.axhline(i - 0.5, color=divider_color, linestyle=divider_ls)
            for j in range(1, n_cols):
                ax.axvline(j - 0.5, color=divider_color, linestyle=divider_ls)

        ax.set_xticks([])
        ax.set_yticks([])

        return ax
