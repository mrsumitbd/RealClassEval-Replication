
class ClassDefinition:

    def __init__(self, name: str):
        self.name = name

    def writeFwdDeclaration(self, target: IO[str], fullInd: str, ind: str) -> None:
        target.write(f"{fullInd}class {self.name};\n")

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, common_namespace: str) -> None:
        target.write(f"{fullInd}class {self.name}\n")
        target.write(f"{fullInd}{{\n")
        target.write(f"{fullInd}{ind}public:\n")
        target.write(f"{fullInd}{ind * 2}{self.name}();\n")
        target.write(f"{fullInd}{ind * 2}~{self.name}();\n")
        target.write(f"{fullInd}}};\n")

    def writeImplDefinition(self, target: IO[str], fullInd: str, ind: str, common_namespace: str) -> None:
        target.write(f"{fullInd}{self.name}::{self.name}()\n")
        target.write(f"{fullInd}{{\n")
        target.write(f"{fullInd}}}\n")
        target.write(f"{fullInd}{self.name}::~{self.name}()\n")
        target.write(f"{fullInd}{{\n")
        target.write(f"{fullInd}}}\n")
