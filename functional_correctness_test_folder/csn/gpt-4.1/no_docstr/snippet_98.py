
import numpy as np


class LCModel:
    def __init__(self):
        self.configs_ = []
        self.times_ = []
        self.losses_ = []

    def fit(self, times, losses, configs=None):
        # times: list of arrays, each array is time points for a config
        # losses: list of arrays, each array is losses for a config
        # configs: list of config identifiers (optional)
        self.times_ = [np.array(t) for t in times]
        self.losses_ = [np.array(l) for l in losses]
        if configs is not None:
            self.configs_ = list(configs)
        else:
            self.configs_ = list(range(len(times)))

    def predict_unseen(self, times, config):
        # Predict loss curve for an unseen config as the mean of all seen curves
        # times: array of time points to predict at
        # config: config identifier (ignored for unseen)
        # Return: array of predicted losses
        # Interpolate all seen curves to the given times, then average
        times = np.array(times)
        interpolated = []
        for t, l in zip(self.times_, self.losses_):
            interp = np.interp(times, t, l, left=l[0], right=l[-1])
            interpolated.append(interp)
        interpolated = np.array(interpolated)
        return np.mean(interpolated, axis=0)

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        # Given a partial curve (obs_times, obs_losses), extend to 'times'
        # by fitting a simple model (e.g., last observed value, or linear extrapolation)
        # If config is in self.configs_, use its curve for extrapolation
        times = np.array(times)
        obs_times = np.array(obs_times)
        obs_losses = np.array(obs_losses)
        if config is not None and config in self.configs_:
            idx = self.configs_.index(config)
            full_t = self.times_[idx]
            full_l = self.losses_[idx]
            # Interpolate/extrapolate using the known curve
            return np.interp(times, full_t, full_l, left=full_l[0], right=full_l[-1])
        else:
            # Use linear extrapolation from last two observed points, or constant if only one
            pred = np.interp(times, obs_times, obs_losses,
                             left=obs_losses[0], right=obs_losses[-1])
            if len(obs_times) >= 2:
                # Linear extrapolation for times > max(obs_times)
                mask = times > obs_times[-1]
                if np.any(mask):
                    x1, x2 = obs_times[-2], obs_times[-1]
                    y1, y2 = obs_losses[-2], obs_losses[-1]
                    if x2 != x1:
                        slope = (y2 - y1) / (x2 - x1)
                        pred[mask] = y2 + slope * (times[mask] - x2)
                    else:
                        pred[mask] = y2
            return pred
