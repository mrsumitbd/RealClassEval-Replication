import numpy as np


class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    def __init__(self, wavespace='wavelength'):
        wavespace = str(wavespace).lower()
        if wavespace not in ('wavelength', 'wavenumber'):
            raise ValueError("wavespace must be 'wavelength' or 'wavenumber'")
        self.wavespace = wavespace
        self.data = {}
        self.channels = ['ch1', 'ch2', 'ch3', 'ch4', 'ch5']
        self._load()

    def _load(self, scale=1.0):
        # Approximate AVHRR/1 channel centers (micrometers) and FWHM (micrometers)
        # ch1: 0.63 µm, ch2: 0.86 µm, ch3: 3.75 µm, ch4: 10.8 µm, ch5: 12.0 µm
        specs = {
            'ch1': {'center': 0.63, 'fwhm': 0.06},
            'ch2': {'center': 0.86, 'fwhm': 0.08},
            'ch3': {'center': 3.75, 'fwhm': 0.7},
            'ch4': {'center': 10.8, 'fwhm': 1.0},
            'ch5': {'center': 12.0, 'fwhm': 1.0},
        }

        def gaussian(x, x0, fwhm):
            sigma = fwhm / (2.0 * np.sqrt(2.0 * np.log(2.0)))
            g = np.exp(-0.5 * ((x - x0) / sigma) ** 2)
            return g

        for ch, s in specs.items():
            c = s['center']
            f = s['fwhm']
            sigma = f / (2.0 * np.sqrt(2.0 * np.log(2.0)))
            x_min = max(1e-6, c - 5 * sigma)
            x_max = c + 5 * sigma
            # Set resolution relative to band width
            step = max(f / 400.0, 1e-4)
            wl = np.arange(x_min, x_max + step, step)
            rsr = gaussian(wl, c, f)
            if rsr.max() > 0:
                rsr = rsr / rsr.max()
            rsr = rsr * float(scale)

            wn = 1e4 / wl  # cm^-1
            # Ensure monotonic increasing x for each representation
            idx_wl = np.argsort(wl)
            wl = wl[idx_wl]
            rsr_wl = rsr[idx_wl]
            idx_wn = np.argsort(wn)
            wn = wn[idx_wn]
            rsr_wn = rsr[idx_wn]

            self.data[ch] = {
                'wavelength': wl,   # micrometers
                'wavenumber': wn,   # cm^-1
                'response_wavelength': rsr_wl,
                'response_wavenumber': rsr_wn,
            }
