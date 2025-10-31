
from typing import IO, Any


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
        ns_open = f"{fullInd}namespace {common_namespace} {{\n" if common_namespace else ""
        ns_close = f"{fullInd}}} // namespace {common_namespace}\n" if common_namespace else ""
        target.write(ns_open)
        target.write(f"{fullInd}class {self.name} {{\n")
        target.write(f"{fullInd}public:\n")
        target.write(f"{fullInd}{ind}/* TODO: add members */\n")
        target.write(f"{fullInd}}};\n")
        target.write(ns_close)

    def writeImplDefinition(self, target: IO[str], fullInd: str, ind: str, common_namespace: str) -> None:
        '''Write definition with implementation.'''
        # For this simple prototype, implementation is identical to definition.
        self.writeDefinition(target, fullInd, ind, common_namespace)
