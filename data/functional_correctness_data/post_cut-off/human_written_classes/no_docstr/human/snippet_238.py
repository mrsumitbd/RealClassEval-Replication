from dataclasses import dataclass

@dataclass(frozen=True, eq=False)
class IRNode:

    def __str__(self):
        from tilus.ir.tools.printer import PrintContext
        printer = PrintContext.current()
        return str(printer(self))

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other