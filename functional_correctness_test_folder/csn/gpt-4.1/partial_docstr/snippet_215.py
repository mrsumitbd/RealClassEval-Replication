
class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''
    # Example RSR data for AVHRR-1 (channels 1-4), in nm and relative response
    # These are illustrative; real data would be more extensive.
    _RSR_DATA = {
        'wavelength': {
            1: [(570, 0.0), (580, 0.1), (600, 0.8), (620, 1.0), (640, 0.7), (660, 0.2), (670, 0.0)],
            2: [(690, 0.0), (700, 0.2), (720, 1.0), (740, 0.8), (760, 0.1), (770, 0.0)],
            3: [(3400, 0.0), (3500, 0.2), (3600, 1.0), (3700, 0.8), (3800, 0.1), (3900, 0.0)],
            4: [(10000, 0.0), (10500, 0.2), (11000, 1.0), (11500, 0.8), (12000, 0.1), (12500, 0.0)],
        },
        'wavenumber': {
            1: [(1e7/670, 0.0), (1e7/660, 0.2), (1e7/640, 0.7), (1e7/620, 1.0), (1e7/600, 0.8), (1e7/580, 0.1), (1e7/570, 0.0)],
            2: [(1e7/770, 0.0), (1e7/760, 0.1), (1e7/740, 0.8), (1e7/720, 1.0), (1e7/700, 0.2), (1e7/690, 0.0)],
            3: [(1e7/3900, 0.0), (1e7/3800, 0.1), (1e7/3700, 0.8), (1e7/3600, 1.0), (1e7/3500, 0.2), (1e7/3400, 0.0)],
            4: [(1e7/12500, 0.0), (1e7/12000, 0.1), (1e7/11500, 0.8), (1e7/11000, 1.0), (1e7/10500, 0.2), (1e7/10000, 0.0)],
        }
    }

    def __init__(self, wavespace='wavelength'):
        if wavespace not in ('wavelength', 'wavenumber'):
            raise ValueError("wavespace must be 'wavelength' or 'wavenumber'")
        self.wavespace = wavespace
        self.rsr = None

    def _load(self, scale=1.0):
        # Loads the RSR data for the selected wavespace, scaling the abscissa if needed
        data = self._RSR_DATA[self.wavespace]
        self.rsr = {}
        for ch, points in data.items():
            abscissa = [p[0] * scale for p in points]
            ordinate = [p[1] for p in points]
            self.rsr[ch] = (abscissa, ordinate)
