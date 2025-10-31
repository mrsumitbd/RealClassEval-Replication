
import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import norm


class LCModel:
    def __init__(self):
        # Initialize an empty list to store observed data
        self.observed_times = []
        self.observed_losses = []
        self.configs = []

    def fit(self, times, losses, configs=None):
        """
        Store observed data for later use.

        Parameters:
        -----------
        times: numpy array
            times where losses were observed
        losses: numpy array
            observed losses
        configs: numpy array or list, optional
            numerical representation of the configs (default is None)
        """
        self.observed_times.append(times)
        self.observed_losses.append(losses)
        if configs is not None:
            self.configs.append(configs)

    def predict_unseen(self, times, config):
        '''
        Predict the loss of an unseen configuration.

        Parameters:
        -----------
        times: numpy array
            times where to predict the loss
        config: numpy array
            the numerical representation of the config

        Returns:
        --------
        mean and variance prediction at input times for the given config
        '''
        # For demonstration, assume a simple nearest neighbor approach
        if not self.configs:
            raise ValueError("No configurations available for prediction.")

        # Find the most similar configuration
        configs_array = np.array(self.configs)
        dists = np.linalg.norm(configs_array - config, axis=1)
        nearest_idx = np.argmin(dists)

        # Interpolate the observed losses for the nearest config
        f = interp1d(self.observed_times[nearest_idx],
                     self.observed_losses[nearest_idx], kind='linear', fill_value="extrapolate")
        mean_pred = f(times)

        # Assume a simple variance model based on the nearest neighbor's residuals
        residuals = self.observed_losses[nearest_idx] - \
            f(self.observed_times[nearest_idx])
        variance_pred = np.full_like(times, np.var(residuals))

        return mean_pred, variance_pred

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        '''
        Extend the model with partial observations.

        Parameters:
        -----------
        times: numpy array
            times where to predict the loss
        obs_times: numpy array
            times where new observations were made
        obs_losses: numpy array
            new observed losses
        config: numpy array, optional
            the numerical representation of the config (default is None)
        '''
        # For demonstration, simply append the new observations
        self.fit(obs_times, obs_losses, config)


# Example usage
if __name__ == "__main__":
    model = LCModel()

    # Example data
    times1 = np.array([1, 2, 3])
    losses1 = np.array([0.1, 0.2, 0.3])
    config1 = np.array([1, 0])

    times2 = np.array([1, 2, 3])
    losses2 = np.array([0.4, 0.5, 0.6])
    config2 = np.array([0, 1])

    model.fit(times1, losses1, config1)
    model.fit(times2, losses2, config2)

    times_pred = np.array([1.5, 2.5])
    config_pred = np.array([1, 0])
    mean, var = model.predict_unseen(times_pred, config_pred)
    print(f"Mean prediction: {mean}, Variance prediction: {var}")

    new_times = np.array([4])
    new_losses = np.array([0.7])
    model.extend_partial(times_pred, new_times, new_losses, config_pred)
