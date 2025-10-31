
import numpy as np
from scipy.optimize import curve_fit


class LCModel:

    def __init__(self):
        self.params = None

    def _learning_curve(self, t, a, b, c):
        return a * (t ** b) + c

    def fit(self, times, losses, configs=None):
        if len(times) < 3:
            raise ValueError(
                "At least 3 data points are required for fitting.")

        try:
            popt, _ = curve_fit(self._learning_curve,
                                times, losses, maxfev=10000)
            self.params = popt
        except RuntimeError:
            self.params = None

    def predict_unseen(self, times, config=None):
        if self.params is None:
            raise ValueError("Model has not been fitted yet.")
        return self._learning_curve(times, *self.params)

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        if len(obs_times) < 3:
            raise ValueError("At least 3 observed data points are required.")

        self.fit(obs_times, obs_losses)
        return self.predict_unseen(times)
