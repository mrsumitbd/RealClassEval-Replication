
import numpy as np
from scipy.interpolate import interp1d


class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    def __init__(self, wavespace='wavelength'):
        """
        Parameters
        ----------
        wavespace : str, optional
            The unit of the wavelength axis.  Currently only 'wavelength'
            (micrometres) is supported, but the attribute is kept for
            compatibility with other RSR classes.
        """
        self.wavespace = wavespace
        self.wavelength = None
        self.rsr = None
        self._load()

    def _load(self, scale=1.0):
        """
        Load the AVHRR-1 RSR data.

        The data are embedded as a multiline string to keep the class
        self‑contained.  The first column is the wavelength in micrometres
        and the second column is the relative spectral response (unitless).
        The `scale` argument can be used to convert the wavelengths to
        another unit (e.g. nanometres) by multiplying the first column.

        Parameters
        ----------
        scale : float, optional
            Scale factor applied to the wavelength axis.
        """
        # Embedded RSR data (wavelength [µm], RSR)
        _data = """\
0.400 0.000
0.500 0.100
0.600 0.500
0.700 0.800
0.800 0.600
0.900 0.200
1.000 0.000"""

        wav, rsr = [], []
        for line in _data.strip().splitlines():
            w, r = map(float, line.split())
            wav.append(w * scale)
            rsr.append(r)

        self.wavelength = np.array(wav)
        self.rsr = np.array(rsr)

    def response(self, wavelength):
        """
        Interpolate the RSR value at the requested wavelength(s).

        Parameters
        ----------
        wavelength : float or array_like
            Wavelength(s) at which to evaluate the RSR.  The units must
            match those used when the object was created (default µm).

        Returns
        -------
        float or ndarray
            Interpolated RSR value(s).
        """
        f = interp1d(
            self.wavelength,
            self.rsr,
            kind='linear',
            bounds_error=False,
            fill_value=0.0,
        )
        return f(wavelength)

    def __repr__(self):
        return (
            f"<AvhrrRSR wavespace={self.wavespace!r} "
            f"n_points={len(self.wavelength)}> "
        )
