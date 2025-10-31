
class Sampleable:

    def __init__(self):
        self.default_sample = None

    def get_sample(self):
        # This method should be overridden by subclasses to provide specific sampling logic
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    def get_default_sample(self):
        return self.default_sample
