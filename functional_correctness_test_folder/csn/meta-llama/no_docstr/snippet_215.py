
import numpy as np


class AvhrrRSR:

    def __init__(self, wavespace='wavelength'):
        """
        Initialize the AvhrrRSR class.

        Parameters
        ----------
        wavespace : str, optional
            The space in which the relative spectral response is defined. 
            Defaults to 'wavelength'.
        """
        self.wavespace = wavespace
        self.rsr = self._load()

    def _load(self, scale=1.0):
        """
        Load the relative spectral response for AVHRR.

        Parameters
        ----------
        scale : float, optional
            A scaling factor for the relative spectral response. 
            Defaults to 1.0.

        Returns
        -------
        dict
            A dictionary containing the relative spectral response for each band.
        """
        # For demonstration purposes, let's assume we have the following RSR data
        # In a real application, this data would be loaded from a file or database
        rsr_data = {
            'AVHRR/1': {
                'channel1': {'wavelength': np.array([0.5, 0.6, 0.7]), 'response': np.array([0.1, 0.8, 0.1])},
                'channel2': {'wavelength': np.array([0.7, 0.8, 0.9]), 'response': np.array([0.2, 0.7, 0.2])},
            },
            'AVHRR/2': {
                'channel1': {'wavelength': np.array([0.55, 0.65, 0.75]), 'response': np.array([0.15, 0.85, 0.15])},
                'channel2': {'wavelength': np.array([0.75, 0.85, 0.95]), 'response': np.array([0.25, 0.75, 0.25])},
            },
            'AVHRR/3': {
                'channel1': {'wavelength': np.array([0.58, 0.68, 0.78]), 'response': np.array([0.18, 0.82, 0.18])},
                'channel2': {'wavelength': np.array([0.78, 0.88, 0.98]), 'response': np.array([0.28, 0.72, 0.28])},
            }
        }

        rsr = {}
        for platform in rsr_data:
            rsr[platform] = {}
            for channel in rsr_data[platform]:
                rsr[platform][channel] = {}
                if self.wavespace == 'wavelength':
                    rsr[platform][channel]['wavelength'] = rsr_data[platform][channel]['wavelength']
                    rsr[platform][channel]['response'] = rsr_data[platform][channel]['response'] * scale
                elif self.wavespace == 'wavenumber':
                    # Convert wavelength to wavenumber
                    wavelength = rsr_data[platform][channel]['wavelength']
                    wavenumber = 1e4 / wavelength  # Assuming wavelength is in microns
                    rsr[platform][channel]['wavenumber'] = wavenumber
                    rsr[platform][channel]['response'] = rsr_data[platform][channel]['response'] * scale
                else:
                    raise ValueError(
                        "Invalid wavespace. It should be either 'wavelength' or 'wavenumber'.")

        return rsr
