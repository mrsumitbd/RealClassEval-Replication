from astropy.modeling.fitting import TRFLSQFitter
from astropy.utils.exceptions import AstropyUserWarning
from astropy.nddata.utils import NoOverlapError, PartialOverlapError
import numpy as np
import warnings
from photutils.utils.cutouts import _overlap_slices as overlap_slices
from photutils.psf.epsf_stars import EPSFStar, EPSFStars, LinkedEPSFStar
from photutils.utils._parameters import SigmaClipSentinelDefault, as_pair, create_default_sigmaclip
from photutils.psf.image_models import ImagePSF, _LegacyEPSFModel
import copy

class EPSFFitter:
    """
    Class to fit an ePSF model to one or more stars.

    Parameters
    ----------
    fitter : `astropy.modeling.fitting.Fitter`, optional
        A `~astropy.modeling.fitting.Fitter` object. If `None`, then the
        default `~astropy.modeling.fitting.TRFLSQFitter` will be used.

    fit_boxsize : int, tuple of int, or `None`, optional
        The size (in pixels) of the box centered on the star to be used
        for ePSF fitting. This allows using only a small number of
        central pixels of the star (i.e., where the star is brightest)
        for fitting. If ``fit_boxsize`` is a scalar then a square box of
        size ``fit_boxsize`` will be used. If ``fit_boxsize`` has two
        elements, they must be in ``(ny, nx)`` order. ``fit_boxsize``
        must have odd values and be greater than or equal to 3 for both
        axes. If `None`, the fitter will use the entire star image.

    **fitter_kwargs : dict, optional
        Any additional keyword arguments (except ``x``, ``y``, ``z``, or
        ``weights``) to be passed directly to the ``__call__()`` method
        of the input ``fitter``.
    """

    def __init__(self, *, fitter=None, fit_boxsize=5, **fitter_kwargs):
        if fitter is None:
            fitter = TRFLSQFitter()
        self.fitter = fitter
        self.fitter_has_fit_info = hasattr(self.fitter, 'fit_info')
        self.fit_boxsize = as_pair('fit_boxsize', fit_boxsize, lower_bound=(3, 0), check_odd=True)
        remove_kwargs = ['x', 'y', 'z', 'weights']
        fitter_kwargs = copy.deepcopy(fitter_kwargs)
        for kwarg in remove_kwargs:
            if kwarg in fitter_kwargs:
                del fitter_kwargs[kwarg]
        self.fitter_kwargs = fitter_kwargs

    def __call__(self, epsf, stars):
        """
        Fit an ePSF model to stars.

        Parameters
        ----------
        epsf : `ImagePSF`
            An ePSF model to be fitted to the stars.

        stars : `EPSFStars` object
            The stars to be fit. The center coordinates for each star
            should be as close as possible to actual centers. For stars
            than contain weights, a weighted fit of the ePSF to the star
            will be performed.

        Returns
        -------
        fitted_stars : `EPSFStars` object
            The fitted stars. The ePSF-fitted center position and flux
            are stored in the ``center`` (and ``cutout_center``) and
            ``flux`` attributes.
        """
        if len(stars) == 0:
            return stars
        if not isinstance(epsf, ImagePSF):
            msg = 'The input epsf must be an ImagePSF'
            raise TypeError(msg)
        epsf = _LegacyEPSFModel(epsf.data, flux=epsf.flux, x_0=epsf.x_0, y_0=epsf.y_0, oversampling=epsf.oversampling, fill_value=epsf.fill_value)
        epsf = epsf.copy()
        fitted_stars = []
        for star in stars:
            if isinstance(star, EPSFStar):
                fitted_star = self._fit_star(epsf, star, self.fitter, self.fitter_kwargs, self.fitter_has_fit_info, self.fit_boxsize)
            elif isinstance(star, LinkedEPSFStar):
                fitted_star = []
                for linked_star in star:
                    fitted_star.append(self._fit_star(epsf, linked_star, self.fitter, self.fitter_kwargs, self.fitter_has_fit_info, self.fit_boxsize))
                fitted_star = LinkedEPSFStar(fitted_star)
                fitted_star.constrain_centers()
            else:
                msg = 'stars must contain only EPSFStar and/or LinkedEPSFStar objects'
                raise TypeError(msg)
            fitted_stars.append(fitted_star)
        return EPSFStars(fitted_stars)

    def _fit_star(self, epsf, star, fitter, fitter_kwargs, fitter_has_fit_info, fit_boxsize):
        """
        Fit an ePSF model to a single star.

        The input ``epsf`` will usually be modified by the fitting
        routine in this function. Make a copy before calling this
        function if the original is needed.
        """
        if fit_boxsize is not None:
            try:
                xcenter, ycenter = star.cutout_center
                large_slc, _ = overlap_slices(star.shape, fit_boxsize, (ycenter, xcenter), mode='strict')
            except (PartialOverlapError, NoOverlapError):
                warnings.warn(f'The star at ({star.center[0]}, {star.center[1]}) cannot be fit because its fitting region extends beyond the star cutout image.', AstropyUserWarning)
                star = copy.deepcopy(star)
                star._fit_error_status = 1
                return star
            data = star.data[large_slc]
            weights = star.weights[large_slc]
            x0 = large_slc[1].start
            y0 = large_slc[0].start
        else:
            data = star.data
            weights = star.weights
            x0 = 0
            y0 = 0
        yy, xx = np.indices(data.shape, dtype=float)
        xx = xx + x0 - star.cutout_center[0]
        yy = yy + y0 - star.cutout_center[1]
        epsf.flux = star.flux
        epsf.x_0 = 0.0
        epsf.y_0 = 0.0
        try:
            fitted_epsf = fitter(model=epsf, x=xx, y=yy, z=data, weights=weights, **fitter_kwargs)
        except TypeError:
            fitted_epsf = fitter(model=epsf, x=xx, y=yy, z=data, **fitter_kwargs)
        fit_error_status = 0
        if fitter_has_fit_info:
            fit_info = copy.copy(fitter.fit_info)
            if 'ierr' in fit_info and fit_info['ierr'] not in [1, 2, 3, 4]:
                fit_error_status = 2
        else:
            fit_info = None
        x_center = star.cutout_center[0] + fitted_epsf.x_0.value
        y_center = star.cutout_center[1] + fitted_epsf.y_0.value
        star = copy.deepcopy(star)
        star.cutout_center = (x_center, y_center)
        star.flux = fitted_epsf.flux.value
        star._fit_info = fit_info
        star._fit_error_status = fit_error_status
        return star