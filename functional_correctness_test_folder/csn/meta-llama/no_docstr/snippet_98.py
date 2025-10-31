
import numpy as np
from scipy.interpolate import interp1d


class LCModel:
    """
    A class used to model learning curves.

    Attributes:
    ----------
    models : dict
        A dictionary to store the models for each configuration.

    Methods:
    -------
    fit(times, losses, configs=None)
        Fits the model to the given data.
    predict_unseen(times, config)
        Predicts the learning curve for a new, unseen configuration.
    extend_partial(times, obs_times, obs_losses, config=None)
        Extends a partially observed learning curve.
    """

    def __init__(self):
        self.models = {}

    def fit(self, times, losses, configs=None):
        """
        Fits the model to the given data.

        Parameters:
        ----------
        times : numpy array
            The time points at which the losses were observed.
        losses : numpy array
            The observed losses.
        configs : numpy array or list, optional
            The configurations corresponding to the losses (default is None).
        """
        if configs is None:
            # If no configs are given, assume there's only one config
            self.models[0] = interp1d(
                times, losses, kind='linear', fill_value="extrapolate")
        else:
            for config, loss in zip(configs, losses):
                if config not in self.models:
                    self.models[config] = []
                self.models[config].append((times, loss))

        # For each config, fit a model
        for config in self.models:
            if config == 0:
                continue
            times_list, losses_list = zip(*self.models[config])
            # For simplicity, we just average the losses at each time point
            # In a real implementation, you'd want to handle this more robustly
            times_avg = np.unique(np.concatenate(times_list))
            losses_avg = np.array([np.mean([loss[np.argmin(np.abs(t - times))] for t, loss in zip(
                times_list, losses_list) if np.any(np.isclose(t, time))]) for time in times_avg])
            self.models[config] = interp1d(
                times_avg, losses_avg, kind='linear', fill_value="extrapolate")

    def predict_unseen(self, times, config):
        """
        Predicts the learning curve for a new, unseen configuration.

        Parameters:
        ----------
        times : numpy array
            The time points at which to predict the losses.
        config : 
            The new configuration.

        Returns:
        -------
        numpy array
            The predicted losses.
        """
        # For an unseen config, we could use the average model or some other strategy
        # Here, we simply average the predictions of all seen configs
        predictions = []
        for model in self.models.values():
            if callable(model):  # Check if model is a function (i.e., interp1d object)
                predictions.append(model(times))
        return np.mean(predictions, axis=0)

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        """
        Extends a partially observed learning curve.

        Parameters:
        ----------
        times : numpy array
            The time points at which to predict the losses.
        obs_times : numpy array
            The time points at which the losses were observed.
        obs_losses : numpy array
            The observed losses.
        config : optional
            The configuration corresponding to the observed losses (default is None).

        Returns:
        -------
        numpy array
            The predicted losses.
        """
        if config is None:
            # If no config is given, assume there's only one config
            config = 0
        if config in self.models:
            # If we have a model for this config, use it to extend the curve
            model = self.models[config]
            pred_losses = model(times)
            # Adjust the prediction based on the observed losses
            obs_model = interp1d(obs_times, obs_losses,
                                 kind='linear', fill_value="extrapolate")
            adjustment = obs_model(times) - model(obs_times)
            adjustment_func = interp1d(
                obs_times, adjustment, kind='linear', fill_value="extrapolate")
            return pred_losses + adjustment_func(times)
        else:
            # If we don't have a model for this config, fit a new model to the observed data
            model = interp1d(obs_times, obs_losses,
                             kind='linear', fill_value="extrapolate")
            return model(times)


# Example usage
if __name__ == "__main__":
    model = LCModel()
    times = np.array([1, 2, 3, 4, 5])
    losses1 = np.array([10, 8, 6, 4, 2])
    losses2 = np.array([12, 9, 7, 5, 3])
    configs = [0, 1]
    losses = [losses1, losses2]
    model.fit(times, losses, configs)
    new_times = np.array([6, 7, 8])
    print(model.predict_unseen(new_times, 2))
    obs_times = np.array([1, 2, 3])
    obs_losses = np.array([11, 9, 7])
    print(model.extend_partial(new_times, obs_times, obs_losses, config=0))
