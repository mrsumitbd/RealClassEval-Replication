
from typing import Optional, List, Tuple, Set
from packaging.tags import Tag


class TargetPython:

    def __init__(self, platforms: Optional[List[str]] = None, py_version_info: Optional[Tuple[int, ...]] = None, abis: Optional[List[str]] = None, implementation: Optional[str] = None) -> None:
        self._platforms = platforms if platforms is not None else []
        self._py_version_info = py_version_info if py_version_info is not None else ()
        self._abis = abis if abis is not None else []
        self._implementation = implementation

    def format_given(self) -> str:
        parts = []
        if self._platforms:
            parts.append(f"platforms={self._platforms}")
        if self._py_version_info:
            parts.append(f"py_version_info={self._py_version_info}")
        if self._abis:
            parts.append(f"abis={self._abis}")
        if self._implementation:
            parts.append(f"implementation={self._implementation}")
        return ", ".join(parts)

    def get_sorted_tags(self) -> List[Tag]:
        return sorted(self.get_unsorted_tags())

    def get_unsorted_tags(self) -> Set[Tag]:
        import packaging.tags
        tags = set()
        for plat in self._platforms or ['any']:
            for abi in self._abis or ['none']:
                for interp in packaging.tags.interpreters_for_platform(plat):
                    if self._implementation and interp.startswith(self._implementation):
                        tags.add(Tag(interp, abi, plat))
                    elif not self._implementation:
                        tags.add(Tag(interp, abi, plat))
        if not self._platforms and not self._abis and not self._implementation:
            tags.add(Tag('py3', 'none', 'any'))
        if self._py_version_info:
            for major, minor in [(self._py_version_info[0], minor) for minor in range(self._py_version_info[1], -1, -1)]:
                for plat in ['any'] if not self._platforms else self._platforms:
                    for abi in ['none'] if not self._abis else self._abis:
                        for interp in [f'cp{major}{minor}', f'py{major}{minor}']:
                            if self._implementation and interp.startswith(self._implementation.lower()):
                                tags.add(Tag(interp, abi, plat))
                            elif not self._implementation:
                                tags.add(Tag(interp, abi, plat))
        return tags
