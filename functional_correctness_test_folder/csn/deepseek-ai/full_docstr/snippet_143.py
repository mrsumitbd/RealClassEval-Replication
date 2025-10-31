
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


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
        if data.ndim != 3:
            raise ValueError('Input data must be a 3D array.')

        n_epsfs, height, width = data.shape
        n_cols = int(np.ceil(np.sqrt(n_epsfs)))
        n_rows = int(np.ceil(n_epsfs / n_cols))

        reshaped_data = np.zeros((n_rows * height, n_cols * width))

        for i in range(n_epsfs):
            row = i // n_cols
            col = i % n_cols
            reshaped_data[row*height:(row+1)*height,
                          col*width:(col+1)*width] = data[i]

        return reshaped_data

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
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure

        if not hasattr(self, 'data'):
            raise AttributeError(
                'The object must have a "data" attribute containing the ePSF grid.')

        data = self.data

        if deltas:
            avg_epsf = np.mean(data, axis=0)
            data = data - avg_epsf[np.newaxis, :, :]

        if peak_norm:
            peak = np.max(np.abs(data))
            data = data / peak

        reshaped_data = self._reshape_grid(data)

        if vmax_scale is None:
            vmax_scale = 0.03 if deltas else 1.0

        vmax = vmax_scale * np.max(np.abs(reshaped_data))

        if deltas:
            vmin = -vmax
            norm = None
        else:
            vmin = vmax / 1e4
            norm = LogNorm(vmin=vmin, vmax=vmax)

        im = ax.imshow(reshaped_data, cmap=cmap, norm=norm,
                       vmin=vmin, vmax=vmax, origin='lower')

        if dividers:
            n_epsfs = data.shape[0]
            n_cols = int(np.ceil(np.sqrt(n_epsfs)))
            n_rows = int(np.ceil(n_epsfs / n_cols))
            height, width = data.shape[1], data.shape[2]

            for i in range(1, n_cols):
                ax.axvline(i * width - 0.5, color=divider_color,
                           linestyle=divider_ls)
            for i in range(1, n_rows):
                ax.axhline(i * height - 0.5, color=divider_color,
                           linestyle=divider_ls)

        ax.set_xticks([])
        ax.set_yticks([])

        return fig
