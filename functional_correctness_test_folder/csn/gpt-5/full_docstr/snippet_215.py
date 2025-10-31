import math
import numpy as np


class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    def __init__(self, wavespace='wavelength'):
        '''Initialize the AVHRR-1 RSR class.'''
        ws = str(wavespace).lower()
        if ws not in ('wavelength', 'wavenumber'):
            raise ValueError("wavespace must be 'wavelength' or 'wavenumber'")
        self.wavespace = ws
        self._centers_um = {
            1: 0.63,   # approximate band centers (micrometers)
            2: 0.86,
            3: 3.75,
            4: 10.8,
        }
        self._fwhm_um = {
            1: 0.10,   # approximate full-width at half-maximum (micrometers)
            2: 0.30,
            3: 0.38,
            4: 1.00,
        }
        self._samples = 1001
        self.data = None

    def _load(self, scale=1.0):
        '''Load the AVHRR RSR data for the band requested.'''
        if not (isinstance(scale, (int, float)) and np.isfinite(scale) and scale > 0):
            raise ValueError("scale must be a positive finite number")

        def gaussian_rsr(lam_um, center_um, fwhm_um):
            # Gaussian defined by FWHM: exp(-4 ln(2) * ((x-mu)^2 / fwhm^2))
            rsr = np.exp(-4.0 * math.log(2.0) *
                         ((lam_um - center_um) ** 2) / (fwhm_um ** 2))
            # normalize to peak of 1.0 then scale
            peak = rsr.max()
            if peak > 0:
                rsr = rsr / peak
            rsr = np.clip(rsr * scale, 0.0, 1.0)
            return rsr

        out = {'wavespace': self.wavespace, 'channels': {}}

        for ch in sorted(self._centers_um):
            c = self._centers_um[ch]
            w = self._fwhm_um[ch]
            lam_min = max(1e-6, c - 3.0 * w)
            lam_max = c + 3.0 * w
            lam = np.linspace(lam_min, lam_max, self._samples, dtype=float)
            rsr = gaussian_rsr(lam, c, w)

            if self.wavespace == 'wavelength':
                x = lam  # micrometers
            else:
                # Convert to wavenumber in cm^-1: nu = 1 / lambda(cm) = 1e4 / lambda(um)
                nu = 1e4 / lam
                # Ensure increasing x for consistency
                order = np.argsort(nu)
                x = nu[order]
                rsr = rsr[order]

            out['channels'][ch] = {'x': x, 'rsr': rsr}

        self.data = out
        return out
