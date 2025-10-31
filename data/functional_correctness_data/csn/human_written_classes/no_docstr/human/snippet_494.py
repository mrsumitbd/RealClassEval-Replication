class FilterExprPredicate:

    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def eval(self, route):
        val = route.attrs.get(self.lhs, None)
        if self.op == '=':
            return val == self.rhs
        elif self.op == '!=':
            return val != self.rhs
        else:
            assert False

    def __repr__(self):
        return 'EvalPred({!r}, {!r}, {!r})'.format(self.op, self.lhs, self.rhs)