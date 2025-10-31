
class AvhrrRSR:

    def __init__(self, wavespace='wavelength'):
        self.wavespace = wavespace
        self.data = None

    def _load(self, scale=1.0):
        # Simulate loading data and applying a scale factor
        if self.wavespace == 'wavelength':
            self.data = [scale * (4.0 + 0.1 * i)
                         for i in range(100)]  # Example data
        elif self.wavespace == 'wavenumber':
            self.data = [scale * (250.0 - 0.25 * i)
                         for i in range(100)]  # Example data
        else:
            raise ValueError("Unsupported wavespace type")
