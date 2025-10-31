import threading


class Connection:
    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def getInstance():
        if Connection._instance is None:
            with Connection._lock:
                if Connection._instance is None:
                    Connection._instance = Connection()
        return Connection._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
