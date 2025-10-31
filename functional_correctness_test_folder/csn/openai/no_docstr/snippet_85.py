class SessionListener:
    def __init__(self):
        self.last_root = None
        self.last_raw = None
        self.last_error = None

    def callback(self, root, raw):
        self.last_root = root
        self.last_raw = raw

    def errback(self, ex):
        self.last_error = ex
