
import numpy as np


class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    def __init__(self, wavespace='wavelength'):
        '''Initialize the AVHRR-1 RSR class.'''
        self.wavespace = wavespace
        self.rsr = None
        self.wavenumbers = None
        self.wavelengths = None
        self._load()

    def _load(self, scale=1.0):
        '''Load the AVHRR RSR data for the band requested.'''
        # Sample data for demonstration purposes
        # In a real implementation, this data would be loaded from a file or database
        avhrr_rsr_data = {
            'wavelength': np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]),
            'rsr': {
                'ch1': np.array([0.1, 0.2, 0.5, 0.8, 0.9, 0.8, 0.5, 0.2]),
                'ch2': np.array([0.05, 0.1, 0.3, 0.6, 0.8, 0.9, 0.8, 0.6]),
                'ch3a': np.array([0.01, 0.05, 0.1, 0.3, 0.6, 0.8, 0.9, 0.8]),
                'ch3b': np.array([0.005, 0.01, 0.05, 0.1, 0.3, 0.6, 0.8, 0.9]),
                'ch4': np.array([0.001, 0.005, 0.01, 0.05, 0.1, 0.3, 0.6, 0.8]),
                'ch5': np.array([0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.3, 0.6])
            }
        }

        self.wavelengths = avhrr_rsr_data['wavelength'] * scale
        # Convert to wavenumbers (cm^-1)
        self.wavenumbers = 1e4 / self.wavelengths

        if self.wavespace == 'wavelength':
            self.rsr = avhrr_rsr_data['rsr']
            self.waves = self.wavelengths
        elif self.wavespace == 'wavenumber':
            self.rsr = avhrr_rsr_data['rsr']
            self.waves = self.wavenumbers
        else:
            raise ValueError(
                "Invalid wavespace. Choose 'wavelength' or 'wavenumber'.")


# Example usage:
if __name__ == "__main__":
    avhrr = AvhrrRSR(wavespace='wavenumber')
    print(avhrr.rsr)
    print(avhrr.waves)
