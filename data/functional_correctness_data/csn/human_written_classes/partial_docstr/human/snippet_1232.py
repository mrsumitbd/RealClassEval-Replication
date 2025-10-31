class ObservingBlockBase:

    def __init__(self, instrument='UNKNOWN', mode='UNKNOWN'):
        self.id = 1
        self.instrument = instrument
        self.mode = mode
        self.frames = []
        self.children = []
        self.parent = None

    def get_sample_frame(self):
        """Return first available frame in observation result"""
        for frame in self.frames:
            return frame