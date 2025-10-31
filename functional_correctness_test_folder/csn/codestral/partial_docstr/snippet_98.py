
import numpy as np


class LCModel:

    def fit(self, times, losses, configs=None):
        self.times = times
        self.losses = losses
        self.configs = configs

    def predict_unseen(self, times, config):
        mean = np.mean(self.losses)
        variance = np.var(self.losses)
        return mean, variance

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        self.times = np.concatenate((self.times, obs_times))
        self.losses = np.concatenate((self.losses, obs_losses))
