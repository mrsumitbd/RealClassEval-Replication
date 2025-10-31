
class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    # AVHRR-1 RSR data for bands 1-4 (wavelength in microns, RSR values)
    # Data from NOAA KLM User's Guide, Table 3.3.1-1 (approximate)
    _rsr_data = {
        'wavelength': {
            1: [
                (0.55, 0.0), (0.58, 0.1), (0.60, 0.5), (0.62, 0.9), (0.64, 1.0),
                (0.66, 0.9), (0.68, 0.5), (0.70, 0.1), (0.72, 0.0)
            ],
            2: [
                (0.70, 0.0), (0.74, 0.1), (0.78, 0.5), (0.82, 0.9), (0.86, 1.0),
                (0.90, 0.9), (0.94, 0.5), (0.98, 0.1), (1.02, 0.0)
            ],
            3: [
                (3.30, 0.0), (3.45, 0.1), (3.60, 0.5), (3.75, 1.0), (3.90, 0.5),
                (4.05, 0.1), (4.20, 0.0)
            ],
            4: [
                (10.30, 0.0), (10.60, 0.1), (10.90,
                                             0.5), (11.20, 1.0), (11.50, 0.5),
                (11.80, 0.1), (12.10, 0.0)
            ]
        },
        'wavenumber': {
            1: [],
            2: [],
            3: [],
            4: []
        }
    }

    def __init__(self, wavespace='wavelength'):
        '''Initialize the AVHRR-1 RSR class.'''
        if wavespace not in ('wavelength', 'wavenumber'):
            raise ValueError("wavespace must be 'wavelength' or 'wavenumber'")
        self.wavespace = wavespace
        self.rsr = None

    def _load(self, scale=1.0):
        '''Load the AVHRR RSR data for the band requested.'''
        import numpy as np

        if self.wavespace == 'wavelength':
            self.rsr = {}
            for band, data in self._rsr_data['wavelength'].items():
                arr = np.array(data)
                arr[:, 0] = arr[:, 0] * scale
                self.rsr[band] = arr
        elif self.wavespace == 'wavenumber':
            self.rsr = {}
            for band, data in self._rsr_data['wavelength'].items():
                arr = np.array(data)
                # Convert wavelength (microns) to wavenumber (cm^-1): wavenumber = 1e4 / wavelength
                wn = 1e4 / (arr[:, 0] * scale)
                rsr_vals = arr[:, 1]
                # Sort by increasing wavenumber
                wn_rsr = np.column_stack((wn, rsr_vals))
                wn_rsr = wn_rsr[wn_rsr[:, 0].argsort()]
                self.rsr[band] = wn_rsr
        else:
            raise ValueError("wavespace must be 'wavelength' or 'wavenumber'")
