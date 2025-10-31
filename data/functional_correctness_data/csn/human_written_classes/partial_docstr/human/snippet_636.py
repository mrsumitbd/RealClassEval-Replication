import numpy as np
from photutils.utils import ShepardIDWInterpolator
from photutils.utils._repr import make_repr
from astropy.units import Quantity

class BkgIDWInterpolator:
    """
    Class to generate a full-sized background and background RMS images
    from lower-resolution mesh images using inverse-distance weighting
    (IDW) interpolation (`~photutils.utils.ShepardIDWInterpolator`).

    This class must be used in concert with the `Background2D` class.

    Parameters
    ----------
    leafsize : float, optional
        The number of points at which the k-d tree algorithm switches
        over to brute-force. ``leafsize`` must be positive. See
        `scipy.spatial.cKDTree` for further information.

    n_neighbors : int, optional
        The maximum number of nearest neighbors to use during the
        interpolation.

    power : float, optional
        The power of the inverse distance used for the interpolation
        weights.

    reg : float, optional
        The regularization parameter. It may be used to control the
        smoothness of the interpolator.
    """

    def __init__(self, *, leafsize=10, n_neighbors=10, power=1.0, reg=0.0):
        self.leafsize = leafsize
        self.n_neighbors = n_neighbors
        self.power = power
        self.reg = reg

    def __repr__(self):
        params = ('leafsize', 'n_neighbors', 'power', 'reg')
        return make_repr(self, params)

    def __call__(self, data, **kwargs):
        """
        Resize the 2D mesh array.

        Parameters
        ----------
        data : 2D `~numpy.ndarray`
            The low-resolution 2D mesh array.

        **kwargs : dict
            Additional keyword arguments passed to the interpolator.

        Returns
        -------
        result : 2D `~numpy.ndarray`
            The resized background or background RMS image.
        """
        data = np.asanyarray(data)
        if isinstance(data, Quantity):
            data = data.value
        if np.ptp(data) == 0:
            return np.full(kwargs['shape'], np.min(data), dtype=kwargs['dtype'])
        yxcen = np.column_stack(kwargs['mesh_yxcen'])
        good_idx = np.where(~kwargs['mesh_nan_mask'])
        data = data[good_idx]
        interp_func = ShepardIDWInterpolator(yxcen, data, leafsize=self.leafsize)
        yi, xi = np.mgrid[0:kwargs['shape'][0], 0:kwargs['shape'][1]]
        yx_indices = np.column_stack((yi.ravel(), xi.ravel()))
        data = interp_func(yx_indices, n_neighbors=self.n_neighbors, power=self.power, reg=self.reg)
        return data.reshape(kwargs['shape'])