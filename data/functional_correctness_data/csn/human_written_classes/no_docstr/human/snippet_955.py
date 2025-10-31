class SimulatorAdapter:

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def world(self):
        return self.lhs.world