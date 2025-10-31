
import numpy as np
from scipy.interpolate import interp1d
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, RBF, WhiteKernel


class LCModel:
    '''
        base class for simple learning curve models
    '''

    def __init__(self):
        self.gpr = GaussianProcessRegressor(
            kernel=ConstantKernel() * RBF() + WhiteKernel(),
            alpha=1e-10,
            n_restarts_optimizer=10
        )

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
        if configs is None:
            X = np.concatenate([np.array([t]).T for t in times])
            y = np.concatenate(losses)
            self.gpr.fit(X, y)
        else:
            X = np.concatenate([np.hstack((np.array([t]).T, np.tile(
                c, (len(t), 1)))) for t, c in zip(times, configs)])
            y = np.concatenate(losses)
            self.gpr.fit(X, y)

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
        X = np.hstack((np.array([times]).T, np.tile(config, (len(times), 1))))
        mean, std = self.gpr.predict(X, return_std=True)
        return mean, std**2

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
        if config is None:
            X = np.array([obs_times]).T
            y = obs_losses
            gpr = GaussianProcessRegressor(
                kernel=ConstantKernel() * RBF() + WhiteKernel(),
                alpha=1e-10,
                n_restarts_optimizer=10
            )
            gpr.fit(X, y)
            X_pred = np.array([times]).T
            mean, std = gpr.predict(X_pred, return_std=True)
        else:
            X = np.hstack((np.array([obs_times]).T,
                          np.tile(config, (len(obs_times), 1))))
            y = obs_losses
            gpr = GaussianProcessRegressor(
                kernel=ConstantKernel() * RBF() + WhiteKernel(),
                alpha=1e-10,
                n_restarts_optimizer=10
            )
            gpr.fit(X, y)
            X_pred = np.hstack(
                (np.array([times]).T, np.tile(config, (len(times), 1))))
            mean, std = gpr.predict(X_pred, return_std=True)

        return mean, std**2
