from tilus.ir.stmt import DeclareStmt, ForStmt, Stmt
from hidet.ir.expr import Constant, Expr, Var, as_expr

class TilusLoopIterable:

    def generate_loop_statement(self, loop_vars: list[Var], body: Stmt) -> Stmt:
        raise NotImplementedError()

    def num_loop_vars(self) -> int:
        raise NotImplementedError()

    def bind_tuple(self) -> bool:
        return False