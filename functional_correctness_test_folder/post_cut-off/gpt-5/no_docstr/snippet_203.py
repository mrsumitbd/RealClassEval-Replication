from typing import Optional, List, Tuple, Set, Iterable
from packaging.tags import Tag, sys_tags


class TargetPython:
    def __init__(
        self,
        platforms: Optional[List[str]] = None,
        py_version_info: Optional[Tuple[int, ...]] = None,
        abis: Optional[List[str]] = None,
        implementation: Optional[str] = None,
    ) -> None:
        self.platforms: Optional[List[str]] = list(
            platforms) if platforms else None
        self.py_version_info: Optional[Tuple[int, ...]] = tuple(
            py_version_info) if py_version_info else None
        self.abis: Optional[List[str]] = list(abis) if abis else None
        self.implementation: Optional[str] = implementation.lower(
        ) if implementation else None

    def format_given(self) -> str:
        parts: List[str] = []
        if self.implementation is not None:
            parts.append(f"implementation={self.implementation}")
        if self.py_version_info is not None:
            parts.append(f"py_version_info={self.py_version_info}")
        if self.abis is not None:
            parts.append("abis=" + ",".join(self.abis))
        if self.platforms is not None:
            parts.append("platforms=" + ",".join(self.platforms))
        return " ".join(parts) if parts else ""

    def _interpreter_matches(self, interpreter: str) -> bool:
        # Parse interpreter into alpha prefix and numeric suffix.
        i = 0
        while i < len(interpreter) and interpreter[i].isalpha():
            i += 1
        impl = interpreter[:i]
        digits = interpreter[i:]

        # Implementation constraint
        if self.implementation is not None and impl != self.implementation:
            return False

        # Version constraints
        if self.py_version_info is None:
            return True

        if not digits:
            return False

        major = self.py_version_info[0] if len(
            self.py_version_info) >= 1 else None
        minor = self.py_version_info[1] if len(
            self.py_version_info) >= 2 else None

        if major is None:
            # If no usable version provided, accept any
            return True

        # Accept digits patterns:
        # - Exact major (e.g., "py3")
        # - Exact major+minor (e.g., "cp311")
        # - For only-major constraint, allow any starting with that major
        if minor is not None:
            return digits == f"{major}{minor}" or digits == f"{major}"
        # Only major specified
        return digits == f"{major}" or digits.startswith(f"{major}")

    def _filter_tags(self, tags: Iterable[Tag]) -> Iterable[Tag]:
        for tag in tags:
            if self.platforms is not None and tag.platform not in self.platforms:
                continue
            if self.abis is not None and tag.abi not in self.abis:
                continue
            if not self._interpreter_matches(tag.interpreter):
                continue
            yield tag

    def get_sorted_tags(self) -> List[Tag]:
        base = list(sys_tags())
        if not any([self.platforms, self.abis, self.implementation, self.py_version_info]):
            return base
        return list(self._filter_tags(base))

    def get_unsorted_tags(self) -> Set[Tag]:
        return set(self.get_sorted_tags())
