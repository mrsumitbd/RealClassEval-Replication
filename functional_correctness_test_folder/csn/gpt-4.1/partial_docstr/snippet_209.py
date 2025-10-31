
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
        if common_namespace:
            target.write(f"{fullInd}namespace {common_namespace} {{\n")
            target.write(f"{fullInd}{ind}class {self.name} {{\n")
            target.write(f"{fullInd}{ind}public:\n")
            target.write(f"{fullInd}{ind}}};\n")
            target.write(f"{fullInd}}} // namespace {common_namespace}\n")
        else:
            target.write(f"{fullInd}class {self.name} {{\n")
            target.write(f"{fullInd}public:\n")
            target.write(f"{fullInd}}};\n")

    def writeImplDefinition(self, target: IO[str], fullInd: str, ind: str, common_namespace: str) -> None:
        '''Write definition with implementation.'''
        if common_namespace:
            target.write(f"{fullInd}namespace {common_namespace} {{\n")
            target.write(f"{fullInd}{ind}class {self.name} {{\n")
            target.write(f"{fullInd}{ind}public:\n")
            target.write(f"{fullInd}{ind}    {self.name}() {{}}\n")
            target.write(f"{fullInd}{ind}    ~{self.name}() {{}}\n")
            target.write(f"{fullInd}{ind}}};\n")
            target.write(f"{fullInd}}} // namespace {common_namespace}\n")
        else:
            target.write(f"{fullInd}class {self.name} {{\n")
            target.write(f"{fullInd}public:\n")
            target.write(f"{fullInd}    {self.name}() {{}}\n")
            target.write(f"{fullInd}    ~{self.name}() {{}}\n")
            target.write(f"{fullInd}}};\n")
