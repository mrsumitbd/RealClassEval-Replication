
from typing import IO, Any


class ClassDefinition:
    def __init__(self, name: str):
        '''Initialize the class definition with a name.'''
        self.name = name

    def writeFwdDeclaration(self, target: IO[str], fullInd: str, ind: str) -> None:
        '''Write forward declaration.'''
        target.write(f"{fullInd}class {self.name};\n")

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, common_namespace: str) -> None:
        '''Write definition of the class.'''
        ns_prefix = f"{common_namespace}::" if common_namespace else ""
        target.write(f"{fullInd}class {ns_prefix}{self.name} {{\n")
        target.write(f"{ind}public:\n")
        target.write(f"{ind}    // TODO: add members\n")
        target.write(f"{fullInd}}};\n")

    def writeImplDefinition(self, target: IO[str], fullInd: str, ind: str, common_namespace: str) -> None:
        '''Write definition with implementation.'''
        ns_prefix = f"{common_namespace}::" if common_namespace else ""
        target.write(f"{fullInd}class {ns_prefix}{self.name} {{\n")
        target.write(f"{ind}public:\n")
        target.write(f"{ind}    {ns_prefix}{self.name}() {{}}\n")
        target.write(f"{ind}    // TODO: add methods\n")
        target.write(f"{fullInd}}};\n")
