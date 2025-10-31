
import numpy as np
import matplotlib.pyplot as plt


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
        # data shape: (ny, nx, psf_shape)
        if data.ndim != 3:
            raise ValueError(
                "Input data must be a 3D numpy array (ny, nx, psf_shape, psf_shape)")
        ny, nx, psf_shape = data.shape
        # If the last dimension is not square, try to infer (ny, nx, sy, sx)
        if psf_shape != data.shape[-1]:
            # Try to reshape to (ny, nx, sy, sx)
            if data.shape[-2] == data.shape[-1]:
                ny, nx, sy, sx = data.shape
                data = data
            else:
                raise ValueError(
                    "Input data must be (ny, nx, sy, sx) or (ny, nx, psf_shape)")
        if data.ndim == 3:
            # (ny, nx, psf_shape) -> (ny, nx, psf_shape, psf_shape)
            psf_shape = data.shape[2]
            data = data.reshape(
                (data.shape[0], data.shape[1], psf_shape, psf_shape))
        ny, nx, sy, sx = data.shape
        # Stack horizontally for each row, then vertically
        rows = [np.hstack([data[j, i] for i in range(nx)]) for j in range(ny)]
        reshaped = np.vstack(rows)
        return reshaped

    def plot_grid(self, *, ax=None, vmax_scale=None, peak_norm=False, deltas=False, cmap='viridis', dividers=True, divider_color='darkgray', divider_ls='-', figsize=None):
        '''
        Plot the grid of ePSF models.
        '''
        # Assume self.epsf_grid is (ny, nx, sy, sx) or (ny, nx, psf_shape)
        if not hasattr(self, 'epsf_grid'):
            raise AttributeError(
                "Class using ModelGridPlotMixin must have an 'epsf_grid' attribute.")
        data = self.epsf_grid
        if data.ndim == 3:
            # (ny, nx, psf_shape) -> (ny, nx, psf_shape, psf_shape)
            psf_shape = data.shape[2]
            data = data.reshape(
                (data.shape[0], data.shape[1], psf_shape, psf_shape))
        ny, nx, sy, sx = data.shape

        # Prepare data for plotting
        if deltas:
            # Show difference from mean ePSF
            mean_epsf = np.mean(data, axis=(0, 1))
            plot_data = data - mean_epsf
            if peak_norm:
                # Normalize by mean peak
                mean_peak = np.max(np.abs(mean_epsf))
                plot_data = plot_data / mean_peak if mean_peak != 0 else plot_data
            vmax_scale = 0.03 if vmax_scale is None else vmax_scale
            vmax = np.max(np.abs(plot_data)) * vmax_scale
            vmin = -vmax
        else:
            plot_data = data.copy()
            if peak_norm:
                # Normalize each ePSF by its own peak
                peaks = np.max(plot_data, axis=(-2, -1), keepdims=True)
                peaks[peaks == 0] = 1
                plot_data = plot_data / peaks
            vmax_scale = 1.0 if vmax_scale is None else vmax_scale
            vmax = np.max(plot_data) * vmax_scale
            vmin = vmax / 1e4

        # Reshape to 2D image
        grid_img = self._reshape_grid(plot_data)

        # Setup figure/axes
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure

        im = ax.imshow(grid_img, origin='lower',
                       cmap=cmap, vmin=vmin, vmax=vmax)
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        # Draw dividers
        if dividers:
            # Vertical dividers
            for i in range(1, nx):
                x = i * sx - 0.5
                ax.axvline(x, color=divider_color, ls=divider_ls, lw=1)
            # Horizontal dividers
            for j in range(1, ny):
                y = j * sy - 0.5
                ax.axhline(y, color=divider_color, ls=divider_ls, lw=1)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('ePSF Grid' + (' (deltas)' if deltas else ''))
        fig.tight_layout()
        return fig
