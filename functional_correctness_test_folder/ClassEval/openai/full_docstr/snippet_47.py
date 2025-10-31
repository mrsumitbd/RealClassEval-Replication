
class Interpolation:
    """
    This is a class that implements the Linear interpolation operation of one-dimensional and two-dimensional data
    """

    def __init__(self):
        pass

    @staticmethod
    def _find_interval(arr, val):
        """
        Find the index i such that arr[i] <= val <= arr[i+1].
        If val is outside the range, clamp to the nearest interval.
        """
        n = len(arr)
        if val <= arr[0]:
            return 0
        if val >= arr[-1]:
            return n - 2
        # binary search
        lo, hi = 0, n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] <= val <= arr[mid + 1]:
                return mid
            if val < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        # fallback
        return max(0, min(n - 2, lo))

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
        if not (len(x) == len(y)):
            raise ValueError("x and y must have the same length")
        result = []
        for xi in x_interp:
            i = Interpolation._find_interval(x, xi)
            x0, x1 = x[i], x[i + 1]
            y0, y1 = y[i], y[i + 1]
            if x1 == x0:
                yi = y0
            else:
                t = (xi - x0) / (x1 - x0)
                yi = y0 + t * (y1 - y0)
            result.append(yi)
        return result

    @staticmethod
    def interpolate_2d(x, y, z, x_interp, y_interp):
        """
        Linear interpolation of two-dimensional data
        :param x: The x-coordinate of the data point, list.
        :param y: The y-coordinate of the data point, list.
        :param z: The z-coordinate of the data point, list of lists.
        :param x_interp: The x-coordinate of the interpolation point, list.
        :param y_interp: The y-coordinate of the interpolation point, list.
        :return: The z-coordinate of the interpolation point, list.
        >>> interpolation = Interpolation()
        >>> interpolation.interpolate_2d([1, 2, 3], [1, 2, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1.5, 2.5], [1.5, 2.5])
        [3.0, 7.0]
        """
        if not (len(x) == len(z[0]) and len(y) == len(z)):
            raise ValueError("Dimensions of x, y, and z must match")
        result = []
        for xi, yi in zip(x_interp, y_interp):
            ix = Interpolation._find_interval(x, xi)
            iy = Interpolation._find_interval(y, yi)
            x0, x1 = x[ix], x[ix + 1]
            y0, y1 = y[iy], y[iy + 1]
            z00 = z[iy][ix]
            z10 = z[iy][ix + 1]
            z01 = z[iy + 1][ix]
            z11 = z[iy + 1][ix + 1]
            if x1 == x0:
                wx = 0.0
            else:
                wx = (xi - x0) / (x1 - x0)
            if y1 == y0:
                wy = 0.0
            else:
                wy = (yi - y0) / (y1 - y0)
            # bilinear interpolation
            zi = (
                (1 - wx) * (1 - wy) * z00
                + wx * (1 - wy) * z10
                + (1 - wx) * wy * z01
                + wx * wy * z11
            )
            result.append(zi)
        return result
