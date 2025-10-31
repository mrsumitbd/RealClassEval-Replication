
from typing import Optional, List, Tuple, Set
from packaging.tags import Tag, sys_tags


class TargetPython:

    def __init__(self, platforms: Optional[List[str]] = None, py_version_info: Optional[Tuple[int, ...]] = None, abis: Optional[List[str]] = None, implementation: Optional[str] = None) -> None:
        self.platforms = platforms or []
        self.py_version_info = py_version_info or (3, 8)
        self.abis = abis or ['cp38']
        self.implementation = implementation or 'cp'

    def format_given(self) -> str:
        return f"Python {self.py_version_info[0]}.{self.py_version_info[1]} on {' '.join(self.platforms)} with ABIs {' '.join(self.abis)} and implementation {self.implementation}"

    def get_sorted_tags(self) -> List[Tag]:
        tags = list(sys_tags())
        filtered_tags = [tag for tag in tags if tag.platform in self.platforms and tag.abi in self.abis and tag.interpreter.startswith(
            self.implementation)]
        return sorted(filtered_tags)

    def get_unsorted_tags(self) -> Set[Tag]:
        tags = list(sys_tags())
        filtered_tags = {tag for tag in tags if tag.platform in self.platforms and tag.abi in self.abis and tag.interpreter.startswith(
            self.implementation)}
        return filtered_tags
