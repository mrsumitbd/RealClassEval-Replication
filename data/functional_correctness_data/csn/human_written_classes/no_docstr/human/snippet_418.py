class LiveTraderAPI:

    def __init__(self, algorithm):
        self.algo = algorithm
        self.prev_context = None

    def __enter__(self):
        self.prev_context = get_context()
        set_context(self.algo)

    def __exit__(self, *args):
        set_context(self.prev_context)