
import numpy as np
import os


class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    def __init__(self, wavespace='wavelength'):
        self.wavespace = wavespace
        self.rsr = None
        self.wavenumber = None
        self.wavelength = None
        self._load()

    def _load(self, scale=1.0):
        avhrr_rsr_dir = os.path.join(
            os.path.dirname(__file__), 'data', 'rsr', 'avhrr')
        avhrr_rsr_file = os.path.join(avhrr_rsr_dir, 'avhrr_rsr.npz')
        data = np.load(avhrr_rsr_file)
        self.wavelength = data['wavelength']
        self.rsr = data['rsr']
        if self.wavespace == 'wavenumber':
            self.wavenumber = 1. / \
                self.wavelength[::-1] * 1e4  # micron to cm-1
            self.rsr = self.rsr[:, ::-1]
        self.wavelength *= scale
        if self.wavenumber is not None:
            self.wavenumber /= scale
