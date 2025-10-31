class RecordingConfig:

    def __init__(self, initial_values, user_config):
        self.initial_values = initial_values
        self.user_config = user_config

    def get_value(self, key, user_config_key=None, default=None):
        return self.initial_values.get(key, self.user_config.get(user_config_key or key, default))