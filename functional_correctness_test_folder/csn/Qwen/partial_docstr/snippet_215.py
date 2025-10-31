
class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    def __init__(self, wavespace='wavelength'):
        self.wavespace = wavespace
        self.data = None

    def _load(self, scale=1.0):
        import numpy as np
        # Example data loading, replace with actual data source
        if self.wavespace == 'wavelength':
            # Example wavelengths in micrometers
            wavelengths = np.array([0.58, 0.66, 0.83, 1.03, 1.20])
            # Example response values
            responses = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
        else:
            raise ValueError("Unsupported wavespace type")

        self.data = (wavelengths * scale, responses * scale)
