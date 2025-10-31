
import numpy as np


class LCModel:
    '''
        base class for simple learning curve models
            '''

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
        # Placeholder implementation
        mean_prediction = np.zeros_like(times)
        variance_prediction = np.ones_like(times)
        return mean_prediction, variance_prediction

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
        # Placeholder implementation
        mean_prediction = np.interp(times, obs_times, obs_losses)
        variance_prediction = np.ones_like(times)
        return mean_prediction, variance_prediction
