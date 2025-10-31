
class LCModel:

    def fit(self, times, losses, configs=None):
        self.times = times
        self.losses = losses
        self.configs = configs

    def predict_unseen(self, times, config):
        # Implement prediction logic here
        pass

    def extend_partial(self, times, obs_times, obs_losses, config=None):
        # Implement partial extension logic here
        pass
