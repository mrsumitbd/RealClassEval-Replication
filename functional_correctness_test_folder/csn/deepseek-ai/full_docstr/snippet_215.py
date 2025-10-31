
import numpy as np
import os


class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    def __init__(self, wavespace='wavelength'):
        '''Initialize the AVHRR-1 RSR class.'''
        self.wavespace = wavespace
        self.bands = {
            'ch1': None,
            'ch2': None,
            'ch3a': None,
            'ch3b': None,
            'ch4': None,
            'ch5': None
        }
        self._load()

    def _load(self, scale=1.0):
        '''Load the AVHRR RSR data for the band requested.'''
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        for band in self.bands:
            filename = os.path.join(data_dir, f'avhrr1_{band}.txt')
            if os.path.exists(filename):
                data = np.loadtxt(filename)
                if self.wavespace == 'wavelength':
                    self.bands[band] = (data[:, 0] * scale, data[:, 1])
                elif self.wavespace == 'wavenumber':
                    self.bands[band] = (1e4 / (data[:, 0] * scale), data[:, 1])
