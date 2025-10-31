
import numpy as np
from scipy.interpolate import interp1d


class AvhrrRSR:
    """
    A minimal implementation of an AVHRR Radiance Spectral Response (RSR) class.
    The class generates a synthetic spectral response curve that can be scaled
    and queried at arbitrary wavelengths.
    """

    def __init__(self, wavespace: str = "wavelength"):
        """
        Parameters
        ----------
        wavespace : str, optional
            The unit of the wavelength axis.  Currently only 'wavelength' is
            supported, but the attribute is kept for compatibility with
            potential future extensions.
        """
        self.wavespace = wavespace
        self._load()

    def _load(self, scale: float = 1.0):
        """
        Load (or generate) the spectral response data.

        The synthetic response is a Gaussian centered at 1.0 µm with a
        standard deviation of 0.3 µm.  The response is scaled by the
        ``scale`` factor.

        Parameters
        ----------
        scale : float, optional
            Multiplicative factor applied to the response curve.
        """
        # Define a wavelength grid from 0.4 to 2.5 µm (1000 points)
        self.wavelengths = np.linspace(0.4, 2.5, 1000)

        # Gaussian response centered at 1.0 µm, sigma = 0.3 µm
        self.response = np.exp(
            -0.5 * ((self.wavelengths - 1.0) / 0.3) ** 2
        ) * scale

        # Create an interpolation function for fast lookup
        self._interp = interp1d(
            self.wavelengths,
            self.response,
            kind="linear",
            bounds_error=False,
            fill_value=0.0,
        )

    def get_response(self, wavelength: float) -> float:
        """
        Return the spectral response at a given wavelength.

        Parameters
        ----------
        wavelength : float
            Wavelength (µm) at which to evaluate the response.

        Returns
        -------
        float
            Interpolated response value.
        """
        return float(self._interp(wavelength))

    def __repr__(self) -> str:
        return (
            f"<AvhrrRSR wavespace={self.wavespace!r} "
            f"points={len(self.wavelengths)}> "
        )
