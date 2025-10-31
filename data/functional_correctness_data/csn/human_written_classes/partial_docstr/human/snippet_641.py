import numpy as np

class SplitCosineBellWindow:
    """
    Class to define a 2D split cosine bell taper function.

    Parameters
    ----------
    alpha : float, optional
        The percentage of array values that are tapered.

    beta : float, optional
        The inner diameter as a fraction of the array size beyond which
        the taper begins. ``beta`` must be less or equal to 1.0.

    Examples
    --------
    .. plot::
        :include-source:

        import matplotlib.pyplot as plt
        from photutils.psf.matching import SplitCosineBellWindow

        taper = SplitCosineBellWindow(alpha=0.4, beta=0.3)
        data = taper((101, 101))
        plt.imshow(data, origin='lower')
        plt.colorbar()

    A 1D cut across the image center:

    .. plot::
        :include-source:

        import matplotlib.pyplot as plt
        from photutils.psf.matching import SplitCosineBellWindow

        taper = SplitCosineBellWindow(alpha=0.4, beta=0.3)
        data = taper((101, 101))
        plt.plot(data[50, :])
    """

    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    def __call__(self, shape):
        """
        Call self as a function to return a 2D window function of the
        given shape.

        Parameters
        ----------
        shape : tuple of int
            The size of the output array along each axis.

        Returns
        -------
        result : 2D `~numpy.ndarray`
            The window function as a 2D array.
        """
        radial_dist = _radial_distance(shape)
        npts = (np.array(shape).min() - 1.0) / 2.0
        r_inner = self.beta * npts
        r = radial_dist - r_inner
        r_taper = int(np.floor(self.alpha * npts))
        if r_taper != 0:
            f = 0.5 * (1.0 + np.cos(np.pi * r / r_taper))
        else:
            f = np.ones(shape)
        f[radial_dist < r_inner] = 1.0
        r_cut = r_inner + r_taper
        f[radial_dist > r_cut] = 0.0
        return f