
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


class ModelGridPlotMixin:

    def _reshape_grid(self, data):
        n = int(np.sqrt(len(data)))
        return data.reshape((n, n))

    def plot_grid(self, *, ax=None, vmax_scale=None, peak_norm=False, deltas=False, cmap='viridis', dividers=True, divider_color='darkgray', divider_ls='-', figsize=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)

        data = self._reshape_grid(self.data)
        n = data.shape[0]

        if peak_norm:
            vmax = np.max(np.abs(data))
            norm = Normalize(vmin=-vmax, vmax=vmax)
        else:
            norm = None

        if vmax_scale is not None:
            vmax = vmax_scale * np.max(np.abs(data))
            norm = Normalize(vmin=-vmax, vmax=vmax)

        im = ax.imshow(data, cmap=cmap, norm=norm)

        if deltas:
            for i in range(n):
                for j in range(n):
                    ax.text(j, i, f'{data[i, j]:.2f}',
                            ha='center', va='center', color='white')

        if dividers:
            for i in range(1, n):
                ax.axhline(i - 0.5, color=divider_color, linestyle=divider_ls)
                ax.axvline(i - 0.5, color=divider_color, linestyle=divider_ls)

        ax.set_xticks(np.arange(n))
        ax.set_yticks(np.arange(n))
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        return im
