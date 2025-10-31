
from typing import IO, Any


class ClassDefinition:

    def __init__(self, name: str):
        self.name = name

    def writeFwdDeclaration(self, target: IO[str], fullInd: str, ind: str) -> None:
        target.write(f"{fullInd}class {self.name};\n")

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, common_namespace: str) -> None:
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
        # Implementation definition is usually empty for a class with no methods
        # But we can write a comment or a placeholder
        if common_namespace:
            target.write(
                f"{fullInd}// Implementation for {common_namespace}::{self.name}\n")
        else:
            target.write(f"{fullInd}// Implementation for {self.name}\n")
