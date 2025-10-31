class Interpolation:
    """
    This is a class that implements the Linear interpolation operation of one-dimensional and two-dimensional data
    """

    def __init__(self):
        pass

    @staticmethod
    def _bracket_indices(arr, val):
        n = len(arr)
        if n < 2:
            raise ValueError(
                "Array must contain at least two points for interpolation.")
        if val <= arr[0]:
            return 0, 1
        if val >= arr[-1]:
            return n - 2, n - 1
        # Binary search
        lo, hi = 0, n - 1
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if arr[mid] == val:
                return max(0, mid - 1), mid
            elif arr[mid] < val:
                lo = mid
            else:
                hi = mid
        return lo, hi

    @staticmethod
    def interpolate_1d(x, y, x_interp):
        """
        Linear interpolation of one-dimensional data
        :param x: The x-coordinate of the data point, list.
        :param y: The y-coordinate of the data point, list.
        :param x_interp: The x-coordinate of the interpolation point, list.
        :return: The y-coordinate of the interpolation point, list.
        >>> interpolation = Interpolation()
        >>> interpolation.interpolate_1d([1, 2, 3], [1, 2, 3], [1.5, 2.5])
        [1.5, 2.5]

        """
        if len(x) != len(y):
            throw = ValueError("x and y must have the same length.")
            raise throw
        if len(x) < 2:
            raise ValueError(
                "At least two data points are required for interpolation.")
        # Sort by x
        order = sorted(range(len(x)), key=lambda i: x[i])
        xs = [float(x[i]) for i in order]
        ys = [float(y[i]) for i in order]

        result = []
        for xi in x_interp:
            xi = float(xi)
            i0, i1 = Interpolation._bracket_indices(xs, xi)
            x0, x1 = xs[i0], xs[i1]
            y0, y1 = ys[i0], ys[i1]
            if x1 == x0:
                yi = y0
            else:
                t = (xi - x0) / (x1 - x0)
                yi = y0 * (1 - t) + y1 * t
            result.append(yi)
        return result

    @staticmethod
    def interpolate_2d(x, y, z, x_interp, y_interp):
        """
        Linear interpolation of two-dimensional data
        :param x: The x-coordinate of the data point, list.
        :param y: The y-coordinate of the data point, list.
        :param z: The z-coordinate of the data point, list of lists, shape (len(y), len(x)).
        :param x_interp: The x-coordinate of the interpolation point, list.
        :param y_interp: The y-coordinate of the interpolation point, list.
        :return: The z-coordinate of the interpolation point, list.
        >>> interpolation = Interpolation()
        >>> interpolation.interpolate_2d([1, 2, 3], [1, 2, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1.5, 2.5], [1.5, 2.5])
        [3.0, 7.0]

        """
        if len(x) < 2 or len(y) < 2:
            raise ValueError("x and y must each contain at least two points.")
        if not isinstance(z, (list, tuple)) or any(not isinstance(row, (list, tuple)) for row in z):
            raise ValueError(
                "z must be a 2D list or tuple of shape (len(y), len(x)).")
        if len(z) != len(y):
            raise ValueError("Number of rows in z must equal len(y).")
        if any(len(row) != len(x) for row in z):
            raise ValueError("Each row in z must have length equal to len(x).")
        if len(x_interp) != len(y_interp):
            raise ValueError(
                "x_interp and y_interp must have the same length.")

        # Convert to floats and sort axes; reorder z accordingly
        x_order = sorted(range(len(x)), key=lambda i: x[i])
        y_order = sorted(range(len(y)), key=lambda i: y[i])
        xs = [float(x[i]) for i in x_order]
        ys = [float(y[j]) for j in y_order]

        # Reorder z: first reorder rows by y, then columns by x
        z_reordered_rows = [z[j] for j in y_order]
        z_sorted = []
        for row in z_reordered_rows:
            z_sorted.append([float(row[i]) for i in x_order])

        results = []
        for xi, yi in zip(x_interp, y_interp):
            xi = float(xi)
            yi = float(yi)
            ix0, ix1 = Interpolation._bracket_indices(xs, xi)
            iy0, iy1 = Interpolation._bracket_indices(ys, yi)

            x0, x1 = xs[ix0], xs[ix1]
            y0, y1 = ys[iy0], ys[iy1]

            z00 = z_sorted[iy0][ix0]
            z10 = z_sorted[iy0][ix1]
            z01 = z_sorted[iy1][ix0]
            z11 = z_sorted[iy1][ix1]

            if x1 == x0 and y1 == y0:
                zi = z00
            elif x1 == x0:
                # Linear along y
                ty = (yi - y0) / (y1 - y0) if y1 != y0 else 0.0
                zi = z00 * (1 - ty) + z01 * ty
            elif y1 == y0:
                # Linear along x
                tx = (xi - x0) / (x1 - x0) if x1 != x0 else 0.0
                zi = z00 * (1 - tx) + z10 * tx
            else:
                tx = (xi - x0) / (x1 - x0)
                ty = (yi - y0) / (y1 - y0)
                # Bilinear interpolation
                z0 = z00 * (1 - tx) + z10 * tx
                z1 = z01 * (1 - tx) + z11 * tx
                zi = z0 * (1 - ty) + z1 * ty

            results.append(zi)

        return results
