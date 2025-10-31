
from typing import IO, Any


class ClassDefinition:
    def __init__(self, name: str):
        """
        Create a new class definition with the given name.
        """
        self.name = name

    def writeFwdDeclaration(self, target: IO[str], fullInd: str, ind: str) -> None:
        """
        Write a forward declaration of the class to the target stream.
        """
        target.write(f"{fullInd}class {self.name};\n")

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, common_namespace: str) -> None:
        """
        Write the full class definition (header) to the target stream.
        """
        target.write(f"{fullInd}namespace {common_namespace} {{\n")
        target.write(f"{fullInd}class {self.name} {{\n")
        target.write(f"{fullInd}{ind}public:\n")
        target.write(f"{fullInd}{ind}    // TODO: add members\n")
        target.write(f"{fullInd}}};\n")
        target.write(f"{fullInd}}}\n")

    def writeImplDefinition(self, target: IO[str], fullInd: str, ind: str, common_namespace: str) -> None:
        """
        Write the implementation section for the class to the target stream.
        """
        target.write(f"{fullInd}// Implementation of {self.name} methods\n")
        target.write(f"{fullInd}namespace {common_namespace} {{\n")
        target.write(f"{fullInd}{ind}// TODO: implement methods\n")
        target.write(f"{fullInd}}}\n")
