class Expr:
    """
    Base class for symbolic expressions in optimization problems.

    Note: This class is currently not being used.
    """

    def __add__(self, other):
        return Add(self, to_expr(other))

    def __mul__(self, other):
        return Mul(self, to_expr(other))

    def __matmul__(self, other):
        return MatMul(self, to_expr(other))

    def __neg__(self):
        return Neg(self)

    def children(self):
        return []

    def pretty(self, indent=0):
        pad = '  ' * indent
        lines = [f'{pad}{self.__class__.__name__}']
        for child in self.children():
            lines.append(child.pretty(indent + 1))
        return '\n'.join(lines)