
from typing import Optional, List, Tuple, Set
from packaging.tags import Tag


class TargetPython:

    def __init__(
        self,
        platforms: Optional[List[str]] = None,
        py_version_info: Optional[Tuple[int, ...]] = None,
        abis: Optional[List[str]] = None,
        implementation: Optional[str] = None
    ) -> None:
        self.platforms = platforms or []
        self.py_version_info = py_version_info or (0,)
        self.abis = abis or []
        self.implementation = implementation or ""

    def format_given(self) -> str:
        parts = []
        if self.py_version_info:
            parts.append(f"version_info={self.py_version_info}")
        if self.abis:
            parts.append(f"abis={self.abis}")
        if self.platforms:
            parts.append(f"platforms={self.platforms}")
        if self.implementation:
            parts.append(f"implementation={self.implementation}")
        return ", ".join(parts)

    def get_sorted_tags(self) -> List[Tag]:
        tags = self.get_unsorted_tags()
        return sorted(tags, key=lambda t: (t.interpreter, t.abi, t.platform))

    def get_unsorted_tags(self) -> Set[Tag]:
        tags = set()
        for platform in self.platforms:
            for abi in self.abis:
                tags.add(Tag(self.implementation, abi, platform))
        return tags
