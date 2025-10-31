
class AvhrrRSR:

    def __init__(self, wavespace='wavelength'):
        self.wavespace = wavespace
        self._rsr_data = None
        self._load()

    def _load(self, scale=1.0):
        import numpy as np
        import os

        # Example data structure; replace with actual data loading logic
        self._rsr_data = {
            'ch1': {
                'wavelength': np.array([0.58, 0.62, 0.66, 0.70]) * scale,
                'response': np.array([0.0, 0.8, 1.0, 0.0]) * scale
            },
            'ch2': {
                'wavelength': np.array([0.72, 0.76, 0.80, 0.84]) * scale,
                'response': np.array([0.0, 0.7, 0.9, 0.0]) * scale
            }
        }
