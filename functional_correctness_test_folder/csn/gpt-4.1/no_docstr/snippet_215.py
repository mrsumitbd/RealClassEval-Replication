
class AvhrrRSR:

    # Example RSR data for demonstration purposes
    # In practice, this would be loaded from a file or database
    _RSR_DATA = {
        'wavelength': [0.58, 0.62, 0.66, 0.70, 0.74],  # micrometers
        'response':  [0.0, 0.5, 1.0, 0.5, 0.0]
    }
    _RSR_DATA_WAVENUMBER = {
        'wavenumber': [1e4/0.74, 1e4/0.70, 1e4/0.66, 1e4/0.62, 1e4/0.58],
        'response':   [0.0, 0.5, 1.0, 0.5, 0.0]
    }

    def __init__(self, wavespace='wavelength'):
        if wavespace not in ('wavelength', 'wavenumber'):
            raise ValueError("wavespace must be 'wavelength' or 'wavenumber'")
        self.wavespace = wavespace
        self.rsr = None

    def _load(self, scale=1.0):
        if self.wavespace == 'wavelength':
            data = self._RSR_DATA
            x = [v * scale for v in data['wavelength']]
            y = data['response']
            self.rsr = list(zip(x, y))
        else:
            data = self._RSR_DATA_WAVENUMBER
            x = [v * scale for v in data['wavenumber']]
            y = data['response']
            self.rsr = list(zip(x, y))
        return self.rsr
