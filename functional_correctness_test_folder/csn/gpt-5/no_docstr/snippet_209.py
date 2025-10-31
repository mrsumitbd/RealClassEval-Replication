from typing import IO, Any


class ClassDefinition:
    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Class name must be a non-empty string.")
        self.name = name.strip()

    def writeFwdDeclaration(self, target: IO[str], fullInd: str, ind: str) -> None:
        target.write(f"{fullInd}class {self.name};\n")

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, common_namespace: str) -> None:
        ns = (common_namespace or "").strip()

        if ns:
            target.write(f"{fullInd}namespace {ns} {{\n")

        target.write(
            f"{fullInd if not ns else fullInd + ind}class {self.name} {{\n")
        target.write(f"{fullInd if not ns else fullInd + ind}{ind}public:\n")
        target.write(
            f"{fullInd if not ns else fullInd + ind}{ind}{ind}{self.name}();\n")
        target.write(
            f"{fullInd if not ns else fullInd + ind}{ind}{ind}~{self.name}();\n")
        target.write(f"{fullInd if not ns else fullInd + ind}}};\n")

        if ns:
            target.write(f"{fullInd}}} // namespace {ns}\n")

    def writeImplDefinition(self, target: IO[str], fullInd: str, ind: str, common_namespace: str) -> None:
        ns = (common_namespace or "").strip()
        scope = f"{ns}::" if ns else ""

        if ns:
            target.write(f"{fullInd}namespace {ns} {{\n")

        target.write(
            f"{fullInd if not ns else fullInd + ind}{scope}{self.name}::{self.name}() {{}}\n")
        target.write(
            f"{fullInd if not ns else fullInd + ind}{scope}{self.name}::~{self.name}() {{}}\n")

        if ns:
            target.write(f"{fullInd}}} // namespace {ns}\n")
