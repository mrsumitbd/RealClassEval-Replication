from scipy.ndimage import zoom
from photutils.utils._repr import make_repr
import numpy as np
from astropy.units import Quantity

class BkgZoomInterpolator:
    """
    Class to generate a full-sized background and background RMS images
    from lower-resolution mesh images using the `~scipy.ndimage.zoom`
    (spline) interpolator.

    This class must be used in concert with the `Background2D` class.

    Parameters
    ----------
    order : int, optional
        The order of the spline interpolation used to resize the
        low-resolution background and background RMS mesh images. The
        value must be an integer in the range 0-5. The default is 3
        (bicubic interpolation).

    mode : {'reflect', 'constant', 'nearest', 'wrap'}, optional
        Points outside the boundaries of the input are filled according
        to the given mode. Default is 'reflect'.

    cval : float, optional
        The value used for points outside the boundaries of the input if
        ``mode='constant'``. Default is 0.0.

    clip : bool, optional
        Whether to clip the output to the range of values in the
        input image. This is enabled by default, since higher order
        interpolation may produce values outside the given input range.

    Notes
    -----
    When resizing the mesh to the full image size, the samples are
    considered as the centers of regularly-spaced grid elements (i.e.,
    `~scipy.ndimage.zoom` ``grid_mode`` is True). This makes makes
    zoom's behavior consistent with `scipy.ndimage.map_coordinates` and
    `skimage.transform.resize`
    """

    def __init__(self, *, order=3, mode='reflect', cval=0.0, clip=True):
        self.order = order
        self.mode = mode
        self.cval = cval
        self.clip = clip

    def __repr__(self):
        params = ('order', 'mode', 'cval', 'clip')
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
        zoom_factor = kwargs['box_size']
        result = zoom(data, zoom_factor, order=self.order, mode=self.mode, cval=self.cval, grid_mode=True)
        result = result[0:kwargs['shape'][0], 0:kwargs['shape'][1]]
        if self.clip:
            minval = np.min(data)
            maxval = np.max(data)
            np.clip(result, minval, maxval, out=result)
        return result