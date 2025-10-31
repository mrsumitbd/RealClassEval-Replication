
class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    def __init__(self, wavespace='wavelength'):
        '''Initialize the AVHRR-1 RSR class.'''
        self.wavespace = wavespace
        self.data = None

    def _load(self, scale=1.0):
        '''Load the AVHRR RSR data for the band requested.'''
        # Simulated loading of data
        if self.wavespace == 'wavelength':
            self.data = [scale * x for x in range(1, 11)]  # Example data
        elif self.wavespace == 'wavenumber':
            self.data = [scale * (100 / x)
                         for x in range(1, 11)]  # Example data
        else:
            raise ValueError("Unsupported wavespace type")
