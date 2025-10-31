from typing import IO, Any


class ClassDefinition:
    '''Prototype of a class.'''

    def __init__(self, name: str):
        '''Initialize the class definition with a name.'''
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        self.name = name

    def writeFwdDeclaration(self, target: IO[str], fullInd: str, ind: str) -> None:
        '''Write forward declaration.'''
        del ind
        target.write(f"{fullInd}class {self.name};\n")

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, common_namespace: str) -> None:
        '''Write definition of the class.'''
        ns_opened = False
        if common_namespace:
            target.write(f"{fullInd}namespace {common_namespace} {{\n")
            ns_opened = True

        target.write(f"{fullInd}class {self.name} {{\n")
        target.write(f"{fullInd}{ind}public:\n")
        target.write(f"{fullInd}{ind}{ind}{self.name}() = default;\n")
        target.write(f"{fullInd}{ind}{ind}virtual ~{self.name}() = default;\n")
        target.write(f"{fullInd}}};\n")

        if ns_opened:
            target.write(f"{fullInd}}} // namespace {common_namespace}\n")

    def writeImplDefinition(self, target: IO[str], fullInd: str, ind: str, common_namespace: str) -> None:
        '''Write definition with implementation.'''
        ns_opened = False
        if common_namespace:
            target.write(f"{fullInd}namespace {common_namespace} {{\n")
            ns_opened = True

        target.write(f"{fullInd}class {self.name} {{\n")
        target.write(f"{fullInd}{ind}public:\n")
        target.write(f"{fullInd}{ind}{ind}{self.name}() {{}}\n")
        target.write(f"{fullInd}{ind}{ind}virtual ~{self.name}() {{}}\n")
        target.write(f"{fullInd}}};\n")

        if ns_opened:
            target.write(f"{fullInd}}} // namespace {common_namespace}\n")
