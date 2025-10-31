class ActiveConfigSettings:
    _current = {}

    def __init__(self, config_settings):
        self._config = config_settings

    def __enter__(self):
        type(self)._current = self._config

    def __exit__(self, exc_type, exc_val, exc_tb):
        type(self)._current = {}

    @classmethod
    def current(cls):
        return cls._current