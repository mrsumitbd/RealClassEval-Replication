
class ClassDefinition:
    '''Prototype of a class.'''

    def __init__(self, name: str):
        '''Initialize the class definition with a name.'''
        self.name = name

    def writeFwdDeclaration(self, target: IO[str], fullInd: str, ind: str) -> None:
        '''Write forward declaration.'''
        target.write(f"{fullInd}class {self.name};\n")

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, common_namespace: str) -> None:
        '''Write definition of the class.'''
        target.write(f"{fullInd}class {self.name} {{\n")
        target.write(f"{ind}public:\n")
        target.write(f"{ind}{ind}{self.name}();\n")
        target.write(f"{ind}{ind}~{self.name}();\n")
        target.write(f"{fullInd}}};\n")

    def writeImplDefinition(self, target: IO[str], fullInd: str, ind: str, common_namespace: str) -> None:
        '''Write definition with implementation.'''
        target.write(f"{fullInd}{self.name}::{self.name}() {{\n")
        target.write(f"{ind}// Constructor implementation\n")
        target.write(f"{fullInd}}}\n\n")
        target.write(f"{fullInd}{self.name}::~{self.name}() {{\n")
        target.write(f"{ind}// Destructor implementation\n")
        target.write(f"{fullInd}}}\n")
