
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
        def linear_interpolate(x0, y0, x1, y1, x):
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

        y_interp = []
        for xi in x_interp:
            for i in range(len(x) - 1):
                if x[i] <= xi <= x[i + 1]:
                    yi = linear_interpolate(x[i], y[i], x[i + 1], y[i + 1], xi)
                    y_interp.append(yi)
                    break
        return y_interp

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
        def linear_interpolate(x0, y0, x1, y1, x):
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

        z_interp = []
        for xi, yi in zip(x_interp, y_interp):
            for i in range(len(x) - 1):
                if x[i] <= xi <= x[i + 1]:
                    for j in range(len(y) - 1):
                        if y[j] <= yi <= y[j + 1]:
                            z00 = z[i][j]
                            z01 = z[i][j + 1]
                            z10 = z[i + 1][j]
                            z11 = z[i + 1][j + 1]
                            x0, x1 = x[i], x[i + 1]
                            y0, y1 = y[j], y[j + 1]
                            z0 = linear_interpolate(x0, z00, x1, z10, xi)
                            z1 = linear_interpolate(x0, z01, x1, z11, xi)
                            zi = linear_interpolate(y0, z0, y1, z1, yi)
                            z_interp.append(zi)
                            break
                    break
        return z_interp
