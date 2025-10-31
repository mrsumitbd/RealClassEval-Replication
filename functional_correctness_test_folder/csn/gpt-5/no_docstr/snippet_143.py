import numpy as np
import math


class ModelGridPlotMixin:

    def _reshape_grid(self, data):
        arr = np.asarray(data)
        # Already 2D
        shape = self._infer_grid_shape(arr.size)
        if arr.ndim == 2:
            if shape is not None and arr.shape != tuple(shape):
                # If data is transposed or mismatched but has same size, try to reshape
                if arr.size == shape[0] * shape[1]:
                    return arr.reshape(shape)
            return arr
        # If 1D or other, try to reshape into grid
        if shape is not None:
            total = shape[0] * shape[1]
            if arr.size == total:
                return arr.reshape(shape)
            # If it is a stacked set of grids, reshape last
            if arr.size % total == 0:
                out = arr.reshape((*shape, arr.size // total))
                # Squeeze trailing singleton if present
                return np.squeeze(out, axis=-1) if out.shape[-1] == 1 else out
        # As a fallback, try square
        n = arr.size
        s = int(round(math.sqrt(n)))
        if s * s == n:
            return arr.reshape((s, s))
        raise ValueError(
            "Cannot reshape data to a 2D grid. Provide compatible data or define grid shape on the object.")

    def plot_grid(self, *, ax=None, vmax_scale=None, peak_norm=False, deltas=False, cmap='viridis', dividers=True, divider_color='darkgray', divider_ls='-', figsize=None):
        import matplotlib.pyplot as plt

        # Retrieve data to plot
        data = getattr(self, 'grid_data', None)
        if data is None:
            data = getattr(self, 'data', None)
        if data is None:
            raise AttributeError(
                "No grid data found. Expected attribute 'grid_data' or 'data' on the object.")
        arr = np.asarray(data)
        grid = self._reshape_grid(arr)

        # Reduce higher dimensions by selecting the first slice if needed
        if grid.ndim > 2:
            grid = grid[..., 0]

        # Transformations
        g = grid.astype(float)
        if deltas:
            g = g - np.nanmin(g)
        if peak_norm:
            peak = np.nanmax(np.abs(g))
            if peak != 0 and np.isfinite(peak):
                g = g / peak

        # vmin/vmax handling
        vmin = np.nanmin(g)
        vmax = np.nanmax(g)
        if vmax_scale is not None and np.isfinite(vmax):
            if peak_norm:
                vmax = 1.0 * float(vmax_scale)
            else:
                vmax = float(vmax) * float(vmax_scale)

        # Figure/Axes
        created_fig = False
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
            created_fig = True
        else:
            fig = ax.figure

        # Determine extent from axes values if available
        ny, nx = g.shape
        xv, yv = self._infer_axis_values(nx, ny)
        origin = 'lower'
        extent = None
        if xv is not None and yv is not None and len(xv) == nx and len(yv) == ny:
            # Compute edges for pcolormesh-like extent
            def edges_from_centers(c):
                c = np.asarray(c, dtype=float)
                if c.size == 1:
                    w = 0.5 if not np.isnan(c[0]) else 0.5
                    return np.array([c[0] - w, c[0] + w])
                d = np.diff(c)
                left = c[0] - d[0] / 2
                right = c[-1] + d[-1] / 2
                mids = c[:-1] + d / 2
                return np.r_[left, mids, right]
            xedges = edges_from_centers(xv)
            yedges = edges_from_centers(yv)
            extent = (xedges[0], xedges[-1], yedges[0], yedges[-1])

        im = ax.imshow(g, origin=origin, cmap=cmap, vmin=vmin, vmax=vmax,
                       aspect='auto', extent=extent, interpolation='nearest')

        # Dividers
        if dividers:
            if extent is None:
                # Draw at cell boundaries in image coordinates
                for i in range(1, nx):
                    ax.axvline(i - 0.5, color=divider_color,
                               linestyle=divider_ls, linewidth=0.6)
                for j in range(1, ny):
                    ax.axhline(j - 0.5, color=divider_color,
                               linestyle=divider_ls, linewidth=0.6)
            else:
                # Draw at edges derived from centers
                xedges = np.linspace(extent[0], extent[1], nx + 1)
                yedges = np.linspace(extent[2], extent[3], ny + 1)
                for i in range(1, nx):
                    ax.axvline(xedges[i], color=divider_color,
                               linestyle=divider_ls, linewidth=0.6)
                for j in range(1, ny):
                    ax.axhline(yedges[j], color=divider_color,
                               linestyle=divider_ls, linewidth=0.6)

        fig.colorbar(im, ax=ax)
        if created_fig and figsize is not None:
            fig.set_size_inches(figsize[0], figsize[1], forward=True)
        return ax

    # Helper methods
    def _infer_grid_shape(self, n_items):
        # Try common attributes for shape
        for attr in ('grid_shape', 'shape'):
            shp = getattr(self, attr, None)
            if isinstance(shp, (tuple, list)) and len(shp) == 2 and all(isinstance(v, (int, np.integer)) for v in shp):
                return (int(shp[0]), int(shp[1]))
        # From counts of x/y vectors
        candidates = [
            ('x_grid', 'y_grid'),
            ('grid_x', 'grid_y'),
            ('x_values', 'y_values'),
            ('xs', 'ys'),
            ('x', 'y'),
        ]
        for xa, ya in candidates:
            xv = getattr(self, xa, None)
            yv = getattr(self, ya, None)
            if xv is not None and yv is not None:
                try:
                    nx = len(xv)
                    ny = len(yv)
                    if nx > 0 and ny > 0:
                        return (ny, nx)
                except Exception:
                    pass
        # From grid coords array of shape (N, 2)
        coords = getattr(self, 'grid_coords', None)
        if coords is not None:
            c = np.asarray(coords)
            if c.ndim == 2 and c.shape[1] >= 2:
                nx = np.unique(c[:, 0]).size
                ny = np.unique(c[:, 1]).size
                if nx * ny == n_items:
                    return (ny, nx)
        # From param grid as sequences
        pg = getattr(self, 'param_grid', None)
        if isinstance(pg, (list, tuple)) and len(pg) >= 2:
            try:
                nx = len(pg[0])
                ny = len(pg[1])
                if nx > 0 and ny > 0:
                    if nx * ny == n_items:
                        return (ny, nx)
            except Exception:
                pass
        # nx, ny attributes
        nx = getattr(self, 'nx', None)
        ny = getattr(self, 'ny', None)
        if isinstance(nx, (int, np.integer)) and isinstance(ny, (int, np.integer)):
            return (int(ny), int(nx))
        # If n_items is a perfect square, use square
        s = int(round(math.sqrt(n_items)))
        if s * s == n_items:
            return (s, s)
        return None

    def _infer_axis_values(self, nx, ny):
        # Returns (x_values, y_values) or (None, None)
        # Prefer explicit attributes
        candidates = [
            ('x_grid', 'y_grid'),
            ('grid_x', 'grid_y'),
            ('x_values', 'y_values'),
            ('xs', 'ys'),
            ('x', 'y'),
        ]
        for xa, ya in candidates:
            xv = getattr(self, xa, None)
            yv = getattr(self, ya, None)
            if xv is not None and yv is not None:
                try:
                    xv = np.asarray(xv).reshape(-1)
                    yv = np.asarray(yv).reshape(-1)
                    if len(xv) == nx and len(yv) == ny:
                        return xv, yv
                except Exception:
                    continue
        return None, None
