
import numpy as np


class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    def __init__(self, wavespace='wavelength'):
        '''Initialize the AVHRR-1 RSR class.'''
        if wavespace not in ('wavelength', 'frequency'):
            raise ValueError("wavespace must be 'wavelength' or 'frequency'")
        self.wavespace = wavespace
        self.data = self._load()

    def _load(self, scale=1.0):
        '''Load the AVHRR RSR data for the band requested.'''
        c = 299792458.0  # speed of light in m/s

        # RSR data in micrometers (µm) and relative response (0–1)
        raw = {
            1: (
                np.array([0.58, 0.60, 0.62, 0.64, 0.66, 0.68]),
                np.array([0.0, 0.2, 0.5, 0.8, 0.5, 0.2]),
            ),
            2: (
                np.array([0.73, 0.75, 0.77, 0.79, 0.81, 0.83]),
                np.array([0.0, 0.3, 0.6, 0.9, 0.6, 0.
