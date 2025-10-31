
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
        if data.ndim != 3:
            raise ValueError("Input data must be a 3D numpy array")
        nrows, ncols = None, None
        # Try to infer grid shape if possible
        if hasattr(self, 'grid_shape'):
            nrows, ncols = self.grid_shape
        else:
            # Try to guess: if data.shape[0] is a perfect square, use sqrt
            n = data.shape[0]
            sq = int(np.sqrt(n))
            if sq * sq == n:
                nrows = ncols = sq
            else:
                # Try to find factors as close as possible
                for i in range(int(np.sqrt(n)), 0, -1):
                    if n % i == 0:
                        nrows = i
                        ncols = n // i
                        break
        if nrows is None or ncols is None:
            raise ValueError("Cannot determine grid shape for ePSF grid")
        # data shape: (nrows*ncols, y, x)
        # Reshape to (nrows, ncols, y, x)
        y, x = data.shape[1], data.shape[2]
        grid = data.reshape((nrows, ncols, y, x))
        # Stack horizontally for each row, then vertically
        rows = [np.hstack(grid[i]) for i in range(nrows)]
        reshaped_data = np.vstack(rows)
        return reshaped_data

    def plot_grid(self, *, ax=None, vmax_scale=None, peak_norm=False, deltas=False, cmap='viridis', dividers=True, divider_color='darkgray', divider_ls='-', figsize=None):
        '''
        Plot the grid of ePSF models.
        '''
        # Get the ePSF data
        if hasattr(self, 'data'):
            data = self.data
        elif hasattr(self, 'epsf_grid'):
            data = self.epsf_grid
        else:
            raise AttributeError(
                "No ePSF data found. Expected attribute 'data' or 'epsf_grid'.")
        data = np.asarray(data)
        if data.ndim != 3:
            raise ValueError("ePSF data must be a 3D numpy array")
        npsfs = data.shape[0]
        # Determine grid shape
        nrows, ncols = None, None
        if hasattr(self, 'grid_shape'):
            nrows, ncols = self.grid_shape
        else:
            n = npsfs
            sq = int(np.sqrt(n))
            if sq * sq == n:
                nrows = ncols = sq
            else:
                for i in range(int(np.sqrt(n)), 0, -1):
                    if n % i == 0:
                        nrows = i
                        ncols = n // i
                        break
        if nrows is None or ncols is None:
            raise ValueError("Cannot determine grid shape for ePSF grid")
        # Optionally normalize by peak
        if peak_norm:
            data = data / np.max(data, axis=(1, 2), keepdims=True)
        # If deltas, subtract mean ePSF
        if deltas:
            mean_epsf = np.mean(data, axis=0)
            data = data - mean_epsf
        # Reshape to 2D grid
        img = self._reshape_grid(data)
        # Set vmin/vmax
        if deltas:
            if vmax_scale is None:
                vmax_scale = 0.03
            vmax = np.max(np.abs(img)) * vmax_scale
            vmin = -vmax
        else:
            if vmax_scale is None:
                vmax_scale = 1.0
            peak = np.max(data)
            vmax = peak * vmax_scale
            vmin = vmax / 1e4
        # Setup figure/axes
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure
        im = ax.imshow(img, origin='lower', cmap=cmap, vmin=vmin, vmax=vmax)
        # Draw dividers
        if dividers:
            ysize, xsize = data.shape[1], data.shape[2]
            for i in range(1, nrows):
                y = i * ysize - 0.5
                ax.axhline(y, color=divider_color, ls=divider_ls, lw=1)
            for j in range(1, ncols):
                x = j * xsize - 0.5
                ax.axvline(x, color=divider_color, ls=divider_ls, lw=1)
        ax.set_xticks([])
        ax.set_yticks([])
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('ePSF Value')
        ax.set_title('ePSF Grid' + (' (Deltas)' if deltas else ''))
        return fig
