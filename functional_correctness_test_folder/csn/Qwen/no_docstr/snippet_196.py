
class Mechanism:

    def __init__(self, mechanism, param=None):
        self.mechanism = mechanism
        self.param = param

    def to_native(self):
        if self.param is not None:
            return f"{self.mechanism}: {self.param}"
        return self.mechanism
