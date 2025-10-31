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

        if not isinstance(data, np.ndarray):
            raise TypeError("data must be a numpy.ndarray")

        if data.ndim == 4:
            ny, nx, h, w = data.shape
            rows = []
            for iy in range(ny):
                rows.append(np.hstack([data[iy, ix] for ix in range(nx)]))
            return np.vstack(rows)

        if data.ndim != 3:
            raise ValueError("data must be 3D (n, h, w) or 4D (ny, nx, h, w)")

        n, h, w = data.shape
        if n == 0:
            return np.empty((0, 0), dtype=data.dtype)

        cols = int(np.ceil(np.sqrt(n)))
        rows = int(np.ceil(n / cols))

        out = np.zeros((rows * h, cols * w), dtype=data.dtype)
        for i in range(n):
            r = i // cols
            c = i % cols
            out[r * h:(r + 1) * h, c * w:(c + 1) * w] = data[i]
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

        def _find_data_attr(obj):
            for name in ('data', 'model_grid', 'grid', 'models', 'epsf_grid'):
                if hasattr(obj, name):
                    arr = getattr(obj, name)
                    if isinstance(arr, np.ndarray):
                        return arr
            raise AttributeError(
                "Could not find a numpy ndarray attribute on self for the ePSF grid (tried: data, model_grid, grid, models, epsf_grid)")

        data = _find_data_attr(self)
        if data.ndim not in (3, 4):
            raise ValueError(
                "ePSF grid must be a 3D array (n, h, w) or 4D array (ny, nx, h, w)")

        # Determine grid layout and tile size for divider lines
        if data.ndim == 4:
            ny, nx, h, w = data.shape
            grid_rows, grid_cols = ny, nx
            tiles = data
        else:
            n, h, w = data.shape
            grid_cols = int(np.ceil(np.sqrt(n)))
            grid_rows = int(np.ceil(n / grid_cols))
            tiles = data

        # Normalize by per-PSF peak if requested
        work = np.array(data, dtype=float, copy=True)
        if peak_norm:
            if work.ndim == 4:
                # per tile max over pixels
                peaks = work.max(axis=(-2, -1))
                peaks[peaks == 0] = 1.0
                work = work / peaks[..., None, None]
            else:
                peaks = work.max(axis=(1, 2))
                peaks[peaks == 0] = 1.0
                work = work / peaks[:, None, None]

        # Compute deltas relative to average ePSF if requested
        if deltas:
            if work.ndim == 4:
                avg = work.mean(axis=(0, 1), keepdims=True)
            else:
                avg = work.mean(axis=0, keepdims=True)
            work = work - avg

        # Determine stretch
        if vmax_scale is None:
            vmax_scale = 0.03 if deltas else 1.0

        # peak based vmax
        if work.ndim == 4:
            peak_val = np.nanmax(np.abs(work)) if deltas else np.nanmax(work)
        else:
            peak_val = np.nanmax(np.abs(work)) if deltas else np.nanmax(work)
        if not np.isfinite(peak_val) or peak_val == 0:
            peak_val = 1.0

        vmax = vmax_scale * peak_val
        vmin = -vmax if deltas else vmax / 1e4

        # Reshape to a single 2D image
        img2d = self._reshape_grid(work)

        # Figure/axes handling
        created_fig = False
        if ax is None:
            if figsize is not None:
                fig, ax = plt.subplots(figsize=figsize)
                created_fig = True
            else:
                ax = plt.gca()
                fig = ax.figure
        else:
            fig = ax.figure

        im = ax.imshow(img2d, origin='lower', cmap=cmap,
                       vmin=vmin, vmax=vmax, interpolation='nearest')

        # Divider lines
        if dividers:
            tile_h, tile_w = h, w
            total_h, total_w = img2d.shape
            for r in range(1, grid_rows):
                y = r * tile_h - 0.5
                ax.axhline(y, color=divider_color, ls=divider_ls, lw=0.5)
            for c in range(1, grid_cols):
                x = c * tile_w - 0.5
                ax.axvline(x, color=divider_color, ls=divider_ls, lw=0.5)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(-0.5, img2d.shape[1] - 0.5)
        ax.set_ylim(-0.5, img2d.shape[0] - 0.5)

        # Add a colorbar if a new figure was created (optional choice)
        # Users can add their own if desired; keeping minimal here.

        return fig
