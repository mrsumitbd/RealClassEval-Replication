
class AvhrrRSR:

    def __init__(self, wavespace='wavelength'):

        self.wavespace = wavespace
        self.rsr = None

    def _load(self, scale=1.0):

        import numpy as np
        import os

        if self.wavespace == 'wavelength':
            self.rsr = np.load(os.path.join(os.path.dirname(
                __file__), 'data', 'avhrr_rsr_wavelength.npy'))
        elif self.wavespace == 'wavenumber':
            self.rsr = np.load(os.path.join(os.path.dirname(
                __file__), 'data', 'avhrr_rsr_wavenumber.npy'))
        else:
            raise ValueError(
                "Invalid wavespace. Choose 'wavelength' or 'wavenumber'.")

        self.rsr = self.rsr * scale
