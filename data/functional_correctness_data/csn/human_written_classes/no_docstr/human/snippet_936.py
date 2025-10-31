class LSystem:

    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.rules = rules

    def compute(self, n):
        state = self.axiom
        for i in range(n):
            state = ''.join(map(lambda c: self.rules.get(c, c), state))
        return state