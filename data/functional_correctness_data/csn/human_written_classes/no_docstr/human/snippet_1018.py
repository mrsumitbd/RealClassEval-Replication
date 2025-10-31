import abc

class BaseForwarder:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def _ensure_connection(self):
        pass

    @abc.abstractmethod
    def handle_logs(self, msgs):
        pass