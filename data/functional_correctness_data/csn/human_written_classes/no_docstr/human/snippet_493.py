class FilterExprConjunction:

    def __init__(self, conj, lhs, rhs):
        self.conj = conj
        self.lhs = lhs
        self.rhs = rhs

    def eval(self, route):
        if self.conj == 'and':
            return self.lhs.eval(route) and self.rhs.eval(route)
        elif self.conj == 'or':
            return self.lhs.eval(route) or self.rhs.eval(route)
        else:
            assert False

    def __repr__(self):
        return 'EvalConj({!r}, {!r}, {!r})'.format(self.conj, self.lhs, self.rhs)