
from typing import List, Optional, Tuple, Set
from packaging.tags import Tag


class TargetPython:

    def __init__(self, platforms: Optional[List[str]] = None, py_version_info: Optional[Tuple[int, ...]] = None, abis: Optional[List[str]] = None, implementation: Optional[str] = None) -> None:
        self.platforms = platforms if platforms is not None else []
        self.py_version_info = py_version_info if py_version_info is not None else ()
        self.abis = abis if abis is not None else []
        self.implementation = implementation if implementation is not None else ''

    def format_given(self) -> str:
        parts = []
        if self.platforms:
            parts.append('platforms: ' + ', '.join(self.platforms))
        if self.py_version_info:
            parts.append('py_version_info: ' +
                         '.'.join(map(str, self.py_version_info)))
        if self.abis:
            parts.append('abis: ' + ', '.join(self.abis))
        if self.implementation:
            parts.append('implementation: ' + self.implementation)
        return '; '.join(parts)

    def get_sorted_tags(self) -> List[Tag]:
        tags = self.get_unsorted_tags()
        return sorted(tags, key=lambda tag: (tag.interpreter, tag.abi, tag.platform))

    def get_unsorted_tags(self) -> Set[Tag]:
        tags = set()
        for platform in self.platforms:
            for abi in self.abis:
                interpreter = f'cp{self.py_version_info[0]}{self.py_version_info[1]}' if self.py_version_info else ''
                tags.add(Tag(interpreter=interpreter,
                         abi=abi, platform=platform))
        return tags
