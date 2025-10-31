import numpy as np

class LookupTable:
    """
    Helper class for two-dimensional look up table

    Lookup table should be saved as an npz file with numpy.savez or
    numpy.savez_compressed. The file should have three arrays:

    * X: log10(x)
    * Y: log10(y)
    * lut: log10(z)

    The instantiated object can be called with arguments (x,y), and the
    interpolated value of z will be returned. The interpolation is done through
    a cubic spline in semi-logarithmic space.
    """

    def __init__(self, filename):
        from scipy.interpolate import RectBivariateSpline
        f_lut = np.load(filename)
        X = f_lut.f.X
        Y = f_lut.f.Y
        lut = f_lut.f.lut
        self.int_lut = RectBivariateSpline(X, Y, 10 ** lut, kx=3, ky=3, s=0)
        self.fname = filename

    def __call__(self, X, Y):
        return self.int_lut(np.log10(X), np.log10(Y)).flatten()