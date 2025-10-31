
import numpy as np


class LCModel:

    def fit(self, times, losses, configs=None):
        # Placeholder for fitting the model
        self.times = times
        self.losses = losses
        self.configs = configs if configs is not None else np.zeros_like(
            losses)
        # Example: Store data for later use
        self.model = {
            'times': times,
            'losses': losses,
            'configs': self.configs
        }

    def predict_unseen(self, times, config):
        # Placeholder for predicting unseen data
        # Example: Return mean and variance of stored losses as prediction
        mean_loss = np.mean(self.losses)
        variance_loss = np.var(self.losses)
        return mean_loss, variance_loss

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        # Placeholder for extending the model with partial data
        # Example: Append new observations to existing data
        if config is not None:
            self.configs = np.append(self.configs, config)
        self.times = np.append(self.times, times)
        self.losses = np.append(self.losses, obs_losses)
        self.model = {
            'times': self.times,
            'losses': self.losses,
            'configs': self.configs
        }
