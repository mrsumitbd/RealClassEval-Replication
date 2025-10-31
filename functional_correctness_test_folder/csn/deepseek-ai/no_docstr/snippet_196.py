
class Mechanism:

    def __init__(self, mechanism, param=None):
        self.mechanism = mechanism
        self.param = param

    def to_native(self):
        return {
            'mechanism': self.mechanism,
            'param': self.param
        }
