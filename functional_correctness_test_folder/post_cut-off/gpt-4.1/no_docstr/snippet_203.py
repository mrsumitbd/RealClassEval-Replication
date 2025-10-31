
from typing import Optional, List, Tuple, Set
from collections import namedtuple

Tag = namedtuple('Tag', ['platform', 'py_version', 'abi', 'implementation'])


class TargetPython:
    def __init__(
        self,
        platforms: Optional[List[str]] = None,
        py_version_info: Optional[Tuple[int, ...]] = None,
        abis: Optional[List[str]] = None,
        implementation: Optional[str] = None
    ) -> None:
        self.platforms = platforms if platforms is not None else []
        self.py_version_info = py_version_info
        self.abis = abis if abis is not None else []
        self.implementation = implementation

    def format_given(self) -> str:
        parts = []
        if self.platforms:
            parts.append(f"platforms={self.platforms}")
        if self.py_version_info:
            parts.append(f"py_version_info={self.py_version_info}")
        if self.abis:
            parts.append(f"abis={self.abis}")
        if self.implementation:
            parts.append(f"implementation={self.implementation}")
        return ", ".join(parts) if parts else "none"

    def get_sorted_tags(self) -> List[Tag]:
        tags = []
        platforms = self.platforms if self.platforms else ['any']
        abis = self.abis if self.abis else ['none']
        py_version = (
            '.'.join(str(x) for x in self.py_version_info)
            if self.py_version_info else 'any'
        )
        implementation = self.implementation if self.implementation else 'cpython'
        for plat in sorted(platforms):
            for abi in sorted(abis):
                tags.append(Tag(plat, py_version, abi, implementation))
        return tags

    def get_unsorted_tags(self) -> Set[Tag]:
        tags = set()
        platforms = self.platforms if self.platforms else ['any']
        abis = self.abis if self.abis else ['none']
        py_version = (
            '.'.join(str(x) for x in self.py_version_info)
            if self.py_version_info else 'any'
        )
        implementation = self.implementation if self.implementation else 'cpython'
        for plat in platforms:
            for abi in abis:
                tags.add(Tag(plat, py_version, abi, implementation))
        return tags
