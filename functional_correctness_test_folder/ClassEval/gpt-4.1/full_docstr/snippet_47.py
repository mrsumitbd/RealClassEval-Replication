
class Interpolation:
    """
    This is a class that implements the Linear interpolation operation of one-dimensional and two-dimensional data
    """

    def __init__(self):
        pass

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
            raise ValueError("x and y must have the same length")
        n = len(x)
        result = []
        for xi in x_interp:
            # Find the interval [x[j], x[j+1]] where xi falls
            if xi <= x[0]:
                j = 0
            elif xi >= x[-1]:
                j = n - 2
            else:
                for k in range(n - 1):
                    if x[k] <= xi <= x[k + 1]:
                        j = k
                        break
            x0, x1 = x[j], x[j + 1]
            y0, y1 = y[j], y[j + 1]
            if x1 == x0:
                yi = y0
            else:
                yi = y0 + (y1 - y0) * (xi - x0) / (x1 - x0)
            result.append(yi)
        return result

    @staticmethod
    def interpolate_2d(x, y, z, x_interp, y_interp):
        """
        Linear interpolation of two-dimensional data
        :param x: The x-coordinate of the data point, list.
        :param y: The y-coordinate of the data point, list.
        :param z: The z-coordinate of the data point, list.
        :param x_interp: The x-coordinate of the interpolation point, list.
        :param y_interp: The y-coordinate of the interpolation point, list.
        :return: The z-coordinate of the interpolation point, list.
        >>> interpolation = Interpolation()
        >>> interpolation.interpolate_2d([1, 2, 3], [1, 2, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1.5, 2.5], [1.5, 2.5])
        [3.0, 7.0]
        """
        if len(z) != len(y) or any(len(row) != len(x) for row in z):
            raise ValueError("z must be a 2D list with shape (len(y), len(x))")
        result = []
        for xi, yi in zip(x_interp, y_interp):
            # Find i such that x[i] <= xi <= x[i+1]
            if xi <= x[0]:
                i = 0
            elif xi >= x[-1]:
                i = len(x) - 2
            else:
                for idx in range(len(x) - 1):
                    if x[idx] <= xi <= x[idx + 1]:
                        i = idx
                        break
            # Find j such that y[j] <= yi <= y[j+1]
            if yi <= y[0]:
                j = 0
            elif yi >= y[-1]:
                j = len(y) - 2
            else:
                for idy in range(len(y) - 1):
                    if y[idy] <= yi <= y[idy + 1]:
                        j = idy
                        break
            x0, x1 = x[i], x[i + 1]
            y0, y1 = y[j], y[j + 1]
            z00 = z[j][i]
            z10 = z[j][i + 1]
            z01 = z[j + 1][i]
            z11 = z[j + 1][i + 1]
            if x1 == x0:
                tx = 0
            else:
                tx = (xi - x0) / (x1 - x0)
            if y1 == y0:
                ty = 0
            else:
                ty = (yi - y0) / (y1 - y0)
            # Bilinear interpolation
            z0 = z00 * (1 - tx) + z10 * tx
            z1 = z01 * (1 - tx) + z11 * tx
            zi = z0 * (1 - ty) + z1 * ty
            result.append(zi)
        return result
