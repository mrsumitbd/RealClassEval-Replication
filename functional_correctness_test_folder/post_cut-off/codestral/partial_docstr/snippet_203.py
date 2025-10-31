
from typing import List, Optional, Tuple, Set
from pip._vendor.packaging.tags import Tag


class TargetPython:

    def __init__(self, platforms: Optional[List[str]] = None, py_version_info: Optional[Tuple[int, ...]] = None, abis: Optional[List[str]] = None, implementation: Optional[str] = None) -> None:
        self.platforms = platforms
        self.py_version_info = py_version_info
        self.abis = abis
        self.implementation = implementation

    def format_given(self) -> str:
        parts = []
        if self.platforms is not None:
            parts.append(f"platforms: {self.platforms}")
        if self.py_version_info is not None:
            parts.append(f"py_version_info: {self.py_version_info}")
        if self.abis is not None:
            parts.append(f"abis: {self.abis}")
        if self.implementation is not None:
            parts.append(f"implementation: {self.implementation}")
        return ", ".join(parts)

    def get_sorted_tags(self) -> List[Tag]:
        tags = self.get_unsorted_tags()
        return sorted(tags, reverse=True)

    def get_unsorted_tags(self) -> Set[Tag]:
        from pip._internal.utils.compatibility_tags import get_supported
        return get_supported(
            platforms=self.platforms,
            python_version=self.py_version_info,
            abis=self.abis,
            implementation=self.implementation,
        )
