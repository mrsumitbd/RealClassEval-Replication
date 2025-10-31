
from typing import List, Optional, Tuple, Set
from packaging.tags import Tag


class TargetPython:

    def __init__(self, platforms: Optional[List[str]] = None, py_version_info: Optional[Tuple[int, ...]] = None, abis: Optional[List[str]] = None, implementation: Optional[str] = None) -> None:
        self.platforms = platforms
        self.py_version_info = py_version_info
        self.abis = abis
        self.implementation = implementation

    def format_given(self) -> str:
        parts = []
        if self.platforms is not None:
            parts.append(f"platforms={self.platforms}")
        if self.py_version_info is not None:
            parts.append(f"py_version_info={self.py_version_info}")
        if self.abis is not None:
            parts.append(f"abis={self.abis}")
        if self.implementation is not None:
            parts.append(f"implementation={self.implementation}")
        return ", ".join(parts)

    def get_sorted_tags(self) -> List[Tag]:
        from packaging.tags import sys_tags
        tags = list(sys_tags())
        if self.py_version_info is not None:
            major = self.py_version_info[0]
            minor = self.py_version_info[1] if len(
                self.py_version_info) > 1 else None
            tags = [t for t in tags if t.interpreter ==
                    f"py{major}{minor if minor is not None else ''}"]
        if self.abis is not None:
            tags = [t for t in tags if t.abi in self.abis]
        if self.implementation is not None:
            tags = [t for t in tags if t.interpreter.startswith(
                self.implementation.lower())]
        return tags

    def get_unsorted_tags(self) -> Set[Tag]:
        return set(self.get_sorted_tags())
