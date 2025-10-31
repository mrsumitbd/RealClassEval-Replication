
from typing import Optional, List, Tuple, Set
from packaging.tags import Tag, sys_tags, compatible_tags
import sys


class TargetPython:

    def __init__(self, platforms: Optional[List[str]] = None, py_version_info: Optional[Tuple[int, ...]] = None, abis: Optional[List[str]] = None, implementation: Optional[str] = None) -> None:
        '''
        :param platforms: A list of strings or None. If None, searches for
            packages that are supported by the current system. Otherwise, will
            find packages that can be built on the platforms passed in. These
            packages will only be downloaded for distribution: they will
            not be built locally.
        :param py_version_info: An optional tuple of ints representing the
            Python version information to use (e.g. `sys.version_info[:3]`).
            This can have length 1, 2, or 3 when provided.
        :param abis: A list of strings or None. This is passed to
            compatibility_tags.py's get_supported() function as is.
        :param implementation: A string or None. This is passed to
            compatibility_tags.py's get_supported() function as is.
        '''
        self.platforms = platforms
        self.py_version_info = py_version_info or sys.version_info[:3]
        self.abis = abis
        self.implementation = implementation

    def format_given(self) -> str:
        '''
        Format the given, non-None attributes for display.
        '''
        given_attributes = []
        if self.platforms is not None:
            given_attributes.append(f"platforms={self.platforms}")
        if self.py_version_info is not None:
            given_attributes.append(f"py_version_info={self.py_version_info}")
        if self.abis is not None:
            given_attributes.append(f"abis={self.abis}")
        if self.implementation is not None:
            given_attributes.append(f"implementation={self.implementation}")
        return ", ".join(given_attributes)

    def get_sorted_tags(self) -> List[Tag]:
        if self.platforms is None:
            return list(sys_tags())
        else:
            return list(compatible_tags(
                python_version=self.py_version_info,
                platforms=self.platforms,
                abis=self.abis,
                interpreter=self.implementation
            ))

    def get_unsorted_tags(self) -> Set[Tag]:
        '''Exactly the same as get_sorted_tags, but returns a set.
        This is important for performance.
        '''
        if self.platforms is None:
            return set(sys_tags())
        else:
            return set(compatible_tags(
                python_version=self.py_version_info,
                platforms=self.platforms,
                abis=self.abis,
                interpreter=self.implementation
            ))
