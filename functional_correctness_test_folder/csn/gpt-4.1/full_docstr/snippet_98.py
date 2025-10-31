
import numpy as np


class LCModel:
    '''
    base class for simple learning curve models
    '''

    def __init__(self):
        self.times = None
        self.losses = None
        self.configs = None
        self.mean_curve = None
        self.var_curve = None
        self.unique_times = None

    def fit(self, times, losses, configs=None):
        '''
        function to train the model on the observed data
        Parameters:
        -----------
        times: list
            list of numpy arrays of the timesteps for each curve
        losses: list
            list of numpy arrays of the loss (the actual learning curve)
        configs: list or None
            list of the configurations for each sample. Each element
            has to be a numpy array. Set to None, if no configuration
            information is available.
        '''
        self.times = times
        self.losses = losses
        self.configs = configs

        # For a simple base model, just compute the mean and variance at each unique time
        all_times = np.concatenate(times)
        all_losses = np.concatenate(losses)
        self.unique_times = np.unique(all_times)
        mean_curve = []
        var_curve = []
        for t in self.unique_times:
            vals = []
            for i in range(len(times)):
                idx = np.where(times[i] == t)[0]
                if len(idx) > 0:
                    vals.extend(losses[i][idx])
            if len(vals) > 0:
                mean_curve.append(np.mean(vals))
                var_curve.append(np.var(vals))
            else:
                mean_curve.append(np.nan)
                var_curve.append(np.nan)
        self.mean_curve = np.array(mean_curve)
        self.var_curve = np.array(var_curve)

    def predict_unseen(self, times, config):
        '''
        predict the loss of an unseen configuration
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
        # As a base model, ignore config and return mean/var at each time
        mean_pred = np.interp(times, self.unique_times,
                              self.mean_curve, left=np.nan, right=np.nan)
        var_pred = np.interp(times, self.unique_times,
                             self.var_curve, left=np.nan, right=np.nan)
        return mean_pred, var_pred

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        '''
        extends a partially observed curve
        Parameters:
        -----------
        times: numpy array
            times where to predict the loss
        obs_times: numpy array
            times where the curve has already been observed
        obs_losses: numpy array
            corresponding observed losses
        config: numpy array
            numerical reperesentation of the config; None if no config
            information is available
        Returns:
        --------
        mean and variance prediction at input times
        '''
        # For observed times, use the observed losses; for others, use mean prediction
        mean_pred, var_pred = self.predict_unseen(times, config)
        for i, t in enumerate(times):
            idx = np.where(obs_times == t)[0]
            if len(idx) > 0:
                mean_pred[i] = obs_losses[idx[0]]
                var_pred[i] = 0.0
        return mean_pred, var_pred
