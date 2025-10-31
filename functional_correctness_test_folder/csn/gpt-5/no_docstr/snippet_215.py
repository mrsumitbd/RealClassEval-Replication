import numpy as np


class AvhrrRSR:

    def __init__(self, wavespace='wavelength'):
        valid = {'wavelength', 'wavenumber'}
        if wavespace not in valid:
            raise ValueError(f"wavespace must be one of {valid}")
        self.wavespace = wavespace
        self._data = None

    def _gaussian(self, x, mu, fwhm):
        sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
        g = np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        return g

    def _rsr_band(self, x, center, width):
        g = self._gaussian(x, center, width)
        g[g < 1e-4] = 0.0
        if g.max() > 0:
            g = g / g.max()
        return g

    def _build_wavelength_grid(self):
        grids = {}
        # Visible/NIR
        grids['B1'] = np.linspace(0.50, 0.80, 601)   # 0.58–0.68
        grids['B2'] = np.linspace(0.70, 1.20, 1001)  # 0.725–1.1
        # AVHRR/3 3A
        grids['B3A'] = np.linspace(1.45, 1.80, 701)  # 1.58–1.64
        # TIR bands
        grids['B3B'] = np.linspace(3.20, 4.20, 1001)  # 3.55–3.93
        grids['B4'] = np.linspace(9.00, 13.00, 1601)  # 10.3–11.3
        grids['B5'] = np.linspace(9.00, 14.00, 2501)  # 11.5–12.5
        return grids

    def _make_rsr_wavelength(self):
        wl = self._build_wavelength_grid()
        rsr = {}
        # Approximate centers and FWHM based on typical AVHRR/3 specs
        specs = {
            'B1':  (0.64, 0.10),
            'B2':  (0.86, 0.25),
            'B3A': (1.61, 0.08),
            'B3B': (3.74, 0.40),
            'B4':  (10.8, 0.90),
            'B5':  (12.0, 1.00),
        }
        for band, x in wl.items():
            c, w = specs[band]
            y = self._rsr_band(x, c, w)
            rsr[band] = (x, y)
        return rsr

    def _convert_to_wavenumber(self, rsr_wl):
        rsr_wn = {}
        for band, (wl_um, resp) in rsr_wl.items():
            wn = 10000.0 / wl_um
            # Interpolation to ensure monotonic ascending domain
            order = np.argsort(wn)
            wn_sorted = wn[order]
            resp_sorted = resp[order]
            rsr_wn[band] = (wn_sorted, resp_sorted)
        return rsr_wn

    def _scale_domain(self, data, scale):
        if scale == 1.0:
            return data
        out = {}
        for band, (x, y) in data.items():
            out[band] = (x * scale, y.copy())
        return out

    def _load(self, scale=1.0):
        rsr_wl = self._make_rsr_wavelength()
        if self.wavespace == 'wavenumber':
            data = self._convert_to_wavenumber(rsr_wl)
        else:
            data = rsr_wl
        data = self._scale_domain(data, scale)
        self._data = data
        return data
