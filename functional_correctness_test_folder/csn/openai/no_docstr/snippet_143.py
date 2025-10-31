
import numpy as np
import matplotlib.pyplot as plt


class ModelGridPlotMixin:
    """
    Mixin providing utilities for reshaping and visualising 2‑D model grids.
    The mixin expects the host class to provide:
        - `self.data`: a 1‑D or 2‑D array containing the grid values.
        - `self.grid_shape`: a tuple (ny, nx) describing the desired 2‑D shape.
    """

    def _reshape_grid(self, data):
        """
        Reshape a 1‑D array into the grid shape defined by `self.grid_shape`.
        If the data is already 2‑D or the shape is not defined, the data is
        returned unchanged.
        """
        shape = getattr(self, "grid_shape", None)
        if shape is None:
            return data
        if data.ndim == 1:
            return data.reshape(shape)
        return data

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
        Plot the model grid using Matplotlib.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            Axes to plot on. If None, a new figure/axes pair is created.
        vmax_scale : float, optional
            Scale factor for the maximum value used in the colour scale.
            If None, the maximum of the data is used.
        peak_norm : bool, default False
            If True, normalise the data by its peak value before plotting.
        deltas : bool, default False
            If True, plot the absolute difference between adjacent cells
            along the x‑axis. The resulting array is padded to the original
            shape.
        cmap : str or Colormap, default 'viridis'
            Colormap to use.
        dividers : bool, default True
            If True, draw grid lines on the plot.
        divider_color : str, default 'darkgray'
            Colour of the grid lines.
        divider_ls : str, default '-'
            Line style of the grid lines.
        figsize : tuple, optional
            Figure size to use when creating a new figure.

        Returns
        -------
        ax : matplotlib.axes.Axes
            The axes containing the plot.
        """
        # Retrieve and reshape data
        if not hasattr(self, "data"):
            raise AttributeError(
                "The host object must provide a 'data' attribute.")
        data = self._reshape_grid(self.data)

        # Normalise by peak if requested
        if peak_norm:
            peak = np.max(np.abs(data))
            if peak != 0:
                data = data / peak

        # Compute deltas if requested
        if deltas:
            # Compute absolute difference along the x‑axis
            diff = np.abs(np.diff(data, axis=1))
            # Pad to original shape
            diff = np.pad(diff, ((0, 0), (0, 1)), mode="constant")
            data = diff

        # Determine vmax for colour scaling
        vmax = None
        if vmax_scale is not None:
            vmax = vmax_scale * np.max(np.abs(data))

        # Create axes if not provided
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)

        # Plot the data
        im = ax.imshow(
            data,
            cmap=cmap,
            vmin=-np.max(np.abs(data)) if peak_norm else None,
            vmax=vmax,
            origin="lower",
        )

        # Add grid lines if requested
        if dividers:
            ax.set_xticks(np.arange(-0.5, data.shape[1], 1), minor=False)
            ax.set_yticks(np.arange(-0.5, data.shape[0], 1), minor=False)
            ax.grid(which="major", color=divider_color, linestyle=divider_ls)

        # Add a colourbar
        plt.colorbar(im, ax=ax)

        return ax
