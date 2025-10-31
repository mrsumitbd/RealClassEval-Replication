from typing import IO, Any, List


class ClassDefinition:
    def __init__(self, name: str):
        '''Initialize the class definition with a name.'''
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        self.name = name

    def writeFwdDeclaration(self, target: IO[str], fullInd: str, ind: str) -> None:
        '''Write forward declaration.'''
        target.write(f"{fullInd}class {self.name};\n")

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, common_namespace: str) -> None:
        '''Write definition of the class.'''
        cur_ind = fullInd
        namespaces = self._split_namespaces(common_namespace)
        cur_ind = self._open_namespaces(target, cur_ind, ind, namespaces)

        # Class definition
        target.write(f"{cur_ind}class {self.name} {{\n")
        target.write(f"{cur_ind}{ind}public:\n")
        target.write(f"{cur_ind}}};\n")

        self._close_namespaces(target, fullInd, ind, namespaces)

    def writeImplDefinition(self, target: IO[str], fullInd: str, ind: str, common_namespace: str) -> None:
        '''Write definition with implementation.'''
        cur_ind = fullInd
        namespaces = self._split_namespaces(common_namespace)
        cur_ind = self._open_namespaces(target, cur_ind, ind, namespaces)

        # Class definition with default implementations
        target.write(f"{cur_ind}class {self.name} {{\n")
        target.write(f"{cur_ind}{ind}public:\n")
        target.write(f"{cur_ind}{ind}{ind}{self.name}() = default;\n")
        target.write(f"{cur_ind}{ind}{ind}~{self.name}() = default;\n")
        target.write(f"{cur_ind}}};\n")

        self._close_namespaces(target, fullInd, ind, namespaces)

    @staticmethod
    def _split_namespaces(ns: str) -> List[str]:
        if not ns:
            return []
        parts = [p.strip() for p in ns.split("::") if p.strip()]
        return parts

    @staticmethod
    def _open_namespaces(target: IO[str], fullInd: str, ind: str, namespaces: List[str]) -> str:
        cur_ind = fullInd
        for ns in namespaces:
            target.write(f"{cur_ind}namespace {ns} {{\n")
            cur_ind += ind
        return cur_ind

    @staticmethod
    def _close_namespaces(target: IO[str], fullInd: str, ind: str, namespaces: List[str]) -> None:
        # Close in reverse order
        cur_ind = fullInd + ind * len(namespaces)
        for ns in reversed(namespaces):
            cur_ind = cur_ind[:-len(ind)]
            target.write(f"{cur_ind}}} // namespace {ns}\n")
