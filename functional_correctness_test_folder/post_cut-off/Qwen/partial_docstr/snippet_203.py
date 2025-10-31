
from typing import Optional, List, Tuple, Set
from packaging.tags import Tag, get_supported


class TargetPython:

    def __init__(self, platforms: Optional[List[str]] = None, py_version_info: Optional[Tuple[int, ...]] = None, abis: Optional[List[str]] = None, implementation: Optional[str] = None) -> None:
        self.platforms = platforms
        self.py_version_info = py_version_info
        self.abis = abis
        self.implementation = implementation

    def format_given(self) -> str:
        attributes = []
        if self.platforms is not None:
            attributes.append(f"platforms: {self.platforms}")
        if self.py_version_info is not None:
            attributes.append(f"py_version_info: {self.py_version_info}")
        if self.abis is not None:
            attributes.append(f"abis: {self.abis}")
        if self.implementation is not None:
            attributes.append(f"implementation: {self.implementation}")
        return ", ".join(attributes)

    def get_sorted_tags(self) -> List[Tag]:
        tags = get_supported(
            platforms=self.platforms,
            py_version_info=self.py_version_info,
            abis=self.abis,
            implementation=self.implementation
        )
        return sorted(tags)

    def get_unsorted_tags(self) -> Set[Tag]:
        tags = get_supported(
            platforms=self.platforms,
            py_version_info=self.py_version_info,
            abis=self.abis,
            implementation=self.implementation
        )
        return set(tags)
