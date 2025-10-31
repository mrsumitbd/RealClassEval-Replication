
class AvhrrRSR:
    '''Container for the NOAA AVHRR-1 RSR data.'''

    def __init__(self, wavespace='wavelength'):
        self.wavespace = wavespace
        self._data = None

    def _load(self, scale=1.0):
        import os
        import numpy as np

        # Define the path to the RSR data file
        data_path = os.path.join(os.path.dirname(
            __file__), 'data', 'avhrr1_rsr.txt')

        # Load the RSR data
        data = np.loadtxt(data_path)

        # Scale the data if necessary
        if scale != 1.0:
            data[:, 1:] = data[:, 1:] * scale

        # Store the data
        self._data = data
