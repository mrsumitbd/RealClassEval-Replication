from typing import Optional
from hidet.ir.expr import BitwiseXor, Expr

class OptionalExpr:

    def __init__(self, expr: Optional[Expr]):
        self.expr: Optional[Expr] = expr

    def empty(self):
        return self.expr is None

    def __add__(self, other):
        if self.expr is None:
            return other
        elif other.expr is None:
            return self
        else:
            return OptionalExpr(self.expr + other.expr)

    def __sub__(self, other):
        if self.expr is None and other.expr is None:
            return OptionalExpr(None)
        elif self.expr is None:
            return OptionalExpr(-other.expr)
        elif other.expr is None:
            return self
        else:
            return OptionalExpr(self.expr - other.expr)

    def __mul__(self, other):
        if self.expr is None or other.expr is None:
            return OptionalExpr(None)
        else:
            return OptionalExpr(self.expr * other.expr)

    def __floordiv__(self, other):
        if self.expr is None or other.expr is None:
            return OptionalExpr(None)
        else:
            return OptionalExpr(self.expr // other.expr)

    def __mod__(self, other):
        if self.expr is None or other.expr is None:
            return OptionalExpr(None)
        else:
            return OptionalExpr(self.expr % other.expr)