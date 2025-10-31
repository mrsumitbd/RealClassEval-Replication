
import numpy as np


class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    def __init__(self, wavespace='wavelength'):
        self.wavespace = wavespace
        self._load()

    def _load(self, scale=1.0):
        # Example data; replace with actual AVHRR-1 RSR data
        self.bands = {
            'ch1': {
                'wavelength': np.array([0.58, 0.62, 0.66, 0.70, 0.74]) * scale,
                'response': np.array([0.0, 0.5, 1.0, 0.5, 0.0])
            },
            'ch2': {
                'wavelength': np.array([0.72, 0.76, 0.80, 0.84, 0.88]) * scale,
                'response': np.array([0.0, 0.3, 0.8, 0.3, 0.0])
            }
        }
