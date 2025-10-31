
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


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
        n_y, n_x, n_psf = data.shape
        reshaped_data = np.zeros((n_y * n_psf, n_x * n_psf))
        for i in range(n_psf):
            for j in range(n_psf):
                reshaped_data[i * n_y:(i + 1) * n_y, j *
                              n_x:(j + 1) * n_x] = data[:, :, i * n_psf + j]
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

        if deltas:
            if vmax_scale is None:
                vmax_scale = 0.03
            data = self.data - np.mean(self.data, axis=2, keepdims=True)
        else:
            if vmax_scale is None:
                vmax_scale = 1.0
            data = self.data

        if peak_norm:
            data = data / np.max(data, axis=(0, 1), keepdims=True)

        reshaped_data = self._reshape_grid(data)
        vmax = np.max(reshaped_data) * vmax_scale

        if deltas:
            vmin = -vmax
        else:
            vmin = vmax / 1e4

        norm = Normalize(vmin=vmin, vmax=vmax)
        im = ax.imshow(reshaped_data, cmap=cmap, norm=norm)

        if dividers:
            n_y, n_x, n_psf = self.data.shape
            for i in range(1, n_psf):
                ax.axhline(i * n_y, color=divider_color, linestyle=divider_ls)
                ax.axvline(i * n_x, color=divider_color, linestyle=divider_ls)

        ax.set_xticks([])
        ax.set_yticks([])
        fig.colorbar(im, ax=ax)

        return fig
