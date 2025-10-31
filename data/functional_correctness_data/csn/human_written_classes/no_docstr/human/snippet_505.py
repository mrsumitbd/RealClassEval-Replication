from sympy.parsing.sympy_parser import parse_expr
from sympy.utilities.lambdify import lambdify

class Expression:

    def __init__(self, text):
        self.txt
        self.expr = parse_expr(text)
        self.npf = self.func()
        self.grad = {sym.__str__(): self.expr.diff(sym) for sym in list(self.expr.free_symbols)}

    def func(self):
        return lambdify(list(self.expr.free_symbols), self.expr, 'numpy')