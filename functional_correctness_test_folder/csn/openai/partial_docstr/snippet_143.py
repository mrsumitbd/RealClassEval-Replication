
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


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
            The 3D or 4D array of ePSF data.
        Returns
        -------
        reshaped_data : `numpy.ndarray`
            The 2D array of ePSF data.
        """
        if data.ndim == 4:
            n_rows, n_cols, h, w = data.shape
            # transpose to (n_rows, h, n_cols, w) then reshape
            reshaped = data.transpose(0, 2, 1, 3).reshape(
                n_rows * h, n_cols * w)
            return reshaped
        elif data.ndim == 3:
            # Assume shape (n_rows, n_cols, n_pixels)
            n_rows, n_cols, n_pixels = data.shape
            # Try to infer square shape
            side = int(np.sqrt(n_pixels))
            if side * side != n_pixels:
                raise ValueError(
                    "3D data with non-square pixel count cannot be reshaped."
                )
            data_4d = data.reshape(n_rows, n_cols, side, side)
            return self._reshape_grid(data_4d)
        else:
            raise ValueError("Data must be a 3D or 4D array.")

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
        ax : `matplotlib.axes.Axes` or `None`, optional
            The matplotlib axes on which to plot. If `None`, then the
            current `~matplotlib.axes.Axes` instance is used.
        vmax_scale : float, optional
            Scale factor to apply to the image stretch limits. This
            value is multiplied by the peak ePSF value to determine the
            plotting ``vmax``. The defaults are 1.0 for plotting the
            ePSF data and 0.03 for plotting the ePSF difference data
            (``deltas=True``). If ``deltas=True``, the ``vmin`` is set
            to ``-vmax``. If ``deltas=False`` the ``vmin`` is set to
            ``vmax`` / 1e4.
        peak_norm : bool, optional
            Whether to normalize the ePSF data by the peak value. The
            default shows the ePSF flux per pixel.
        deltas : bool, optional
            Set to `True` to show the differences between each ePSF
            and the average ePSF.
        cmap : str or `matplotlib.colors.Colormap`, optional
            The colormap to use. The default is 'viridis'.
        dividers : bool, optional
            Whether to show divider lines between the ePSFs.
        divider_color, divider_ls : str, optional
            Matplotlib color and linestyle options for the divider
            lines between ePSFs. These keywords have no effect unless
            ``show_dividers=True``.
        figsize : (float, float), optional
            The figure (width, height) in inches.
        Returns
        -------
        fig : `matplotlib.figure.Figure`
            The matplotlib figure object. This will be the current
            figure if ``ax=None``. Use ``fig.savefig()`` to save the
            figure to a file.
        """
        # Retrieve the grid data from the instance
        if not hasattr(self, "grid_data"):
            raise AttributeError(
                "The instance must have a 'grid_data' attribute containing the ePSF grid."
            )
        data = self.grid_data

        # Compute deltas if requested
        if deltas:
            # Compute mean over the grid
            mean_epsf = np.mean(data, axis=(0, 1))
            data = data - mean_epsf
            peak = np.max(np.abs(data))
        else:
            peak = np.max(data)

        # Normalize by peak if requested
        if peak_norm:
            data = data / peak

        # Determine default vmax_scale
        if vmax_scale is None:
            vmax_scale = 0.03 if deltas else 1.0

        vmax = vmax_scale * peak
        vmin = -vmax if deltas else vmax / 1e4

        # Reshape the grid for plotting
        reshaped = self._reshape_grid(data)

        # Create figure and axes if needed
        if ax is None:
            if figsize is not None:
                fig, ax = plt.subplots(figsize=figsize)
            else:
                fig = plt.gcf()
                ax = plt.gca
