class BaseComponent:

    def __init__(self, base_uri, config, timeout):
        self.base_uri = base_uri
        self.config = config
        self.timeout = timeout

    @property
    def session(self):
        return ZoomSession(self.config)