class EvalSignOp:
    """Class to evaluate expressions with a leading + or - sign"""

    def __init__(self, tokens):
        self.sign, self.value = tokens[0]

    def eval(self):
        mult = {'+': 1, '-': -1}[self.sign]
        return mult * self.value.eval()