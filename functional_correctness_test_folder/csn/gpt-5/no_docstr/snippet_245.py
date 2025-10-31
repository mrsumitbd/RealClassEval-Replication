class Sampleable:

    def __init__(self):
        self._sampler = None
        self._default_sample = {}

    def get_sample(self):
        if callable(self._sampler):
            try:
                sample = self._sampler()
                return sample if sample is not None else self.get_default_sample()
            except Exception:
                return self.get_default_sample()
        return self.get_default_sample()

    def get_default_sample(self):
        import copy
        return copy.deepcopy(self._default_sample)
