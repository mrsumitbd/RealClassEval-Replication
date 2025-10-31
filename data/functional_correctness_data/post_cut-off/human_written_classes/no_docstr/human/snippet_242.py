from tilus.ir.func import Function
from tilus.ir.prog import Program

class Pass:

    def __init__(self) -> None:
        self.name: str = self.__class__.__name__.removesuffix('Pass')

    def __call__(self, prog: Program) -> Program:
        return self.process_program(prog)

    def process_program(self, program: Program) -> Program:
        functions: dict[str, Function] = {name: self.process_function(func) for name, func in program.functions.items()}
        if all((a is b for a, b in zip(functions.values(), program.functions.values()))):
            return program
        else:
            return Program.create(functions)

    def process_function(self, function: Function) -> Function:
        raise NotImplementedError()