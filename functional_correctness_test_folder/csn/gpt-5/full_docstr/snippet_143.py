class ModelGridPlotMixin:
    '''
    Mixin class to plot a grid of ePSF models.
    '''

    def _reshape_grid(self, data):
        '''
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
        '''
        import numpy as np

        if data is None:
            raise ValueError("data must not be None")
        arr = np.asarray(data)
        if arr.ndim != 3:
            raise ValueError("data must be a 3D array with shape (n, ny, nx)")

        n, ny, nx = arr.shape

        def best_grid(nmodels):
            import math
            # choose rows as the largest divisor of n <= sqrt(n)
            r = int(math.floor(math.sqrt(nmodels)))
            while r > 1 and nmodels % r != 0:
                r -= 1
            rows = r if nmodels % r == 0 else 1
            cols = nmodels // rows
            return rows, cols

        rows, cols = best_grid(n)
        # pad with zeros if needed to fill last row
        total = rows * cols
        if total != n:
            pad = total - n
            pad_block = np.zeros((pad, ny, nx), dtype=arr.dtype)
            arr = np.concatenate((arr, pad_block), axis=0)

        # reshape and tile
        grid = arr.reshape(rows, cols, ny, nx)
        out = np.block([[grid[i, j] for j in range(cols)]
                       for i in range(rows)])
        return out

    def plot_grid(self, *, ax=None, vmax_scale=None, peak_norm=False, deltas=False, cmap='viridis', dividers=True, divider_color='darkgray', divider_ls='-', figsize=None):
        '''
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
        Notes
        -----
        This method returns a figure object. If you are using this
        method in a script, you will need to call ``plt.show()`` to
        display the figure. If you are using this method in a Jupyter
        notebook, the figure will be displayed automatically.
        When in a notebook, if you do not store the return value of this
        function, the figure will be displayed twice due to the REPL
        automatically displaying the return value of the last function
        call. Alternatively, you can append a semicolon to the end of
        the function call to suppress the display of the return value.
        '''
        import numpy as np
        import matplotlib.pyplot as plt

        def get_grid_data(obj):
            # Try common attribute/method names
            for name in ('data', '_data', 'grid', 'array', 'models'):
                if hasattr(obj, name):
                    val = getattr(obj, name)
                    val = val() if callable(val) else val
                    if val is not None:
                        return np.asarray(val)
            raise AttributeError(
                "Could not find grid data on the object. Expected an attribute like 'data'.")

        data = get_grid_data(self)
        data = np.asarray(data)
        if data.ndim != 3:
            raise ValueError(
                "Grid data must be a 3D array with shape (n, ny, nx)")

        n, ny, nx = data.shape

        if peak_norm:
            peaks = np.nanmax(np.where(np.isfinite(
                data), data, -np.inf), axis=(1, 2))
            peaks[~np.isfinite(peaks)] = 1.0
            peaks[peaks == 0] = 1.0
            data = data / peaks[:, None, None]

        if deltas:
            avg = np.nanmean(data, axis=0)
            data = data - avg

        if vmax_scale is None:
            vmax_scale = 0.03 if deltas else 1.0

        if deltas:
            peak = np.nanmax(np.abs(data))
            vmax = vmax_scale * (peak if np.isfinite(peak)
                                 and peak > 0 else 1.0)
            vmin = -vmax
        else:
            peak = np.nanmax(data)
            vmax = vmax_scale * (peak if np.isfinite(peak)
                                 and peak > 0 else 1.0)
            vmin = vmax / 1e4

        # Determine rows/cols used for tiling (must match _reshape_grid)
        def best_grid(nmodels):
            import math
            r = int(math.floor(math.sqrt(nmodels)))
            while r > 1 and nmodels % r != 0:
                r -= 1
            rows = r if nmodels % r == 0 else 1
            cols = nmodels // rows
            return rows, cols

        rows, cols = best_grid(n)
        total = rows * cols
        pad = 0
        if total != n:
            pad = total - n
            pad_block = np.zeros((pad, ny, nx), dtype=data.dtype)
            plot_data = np.concatenate((data, pad_block), axis=0)
        else:
            plot_data = data

        tiled = self._reshape_grid(plot_data)

        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
        else:
            fig = ax.figure

        im = ax.imshow(tiled, origin='lower', cmap=cmap,
                       vmin=vmin, vmax=vmax, interpolation='nearest')
        ax.set_xticks([])
        ax.set_yticks([])

        if dividers:
            # draw lines between stamps
            for r in range(1, rows):
                y = r * ny
                ax.hlines(y - 0.5, -0.5, cols * nx - 0.5,
                          colors=divider_color, linestyles=divider_ls, linewidth=0.8)
            for c in range(1, cols):
                x = c * nx
                ax.vlines(x - 0.5, -0.5, rows * ny - 0.5,
                          colors=divider_color, linestyles=divider_ls, linewidth=0.8)

        fig.tight_layout()
        return fig
