
from typing import Optional, List, Tuple, Set
from packaging.tags import Tag, compatible_tags, cpython_tags
import sys
import warnings


class TargetPython:
    '''
    Encapsulates the properties of a Python interpreter one is targeting
    for a package install, download, etc.
    '''

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
        self.py_version_info = py_version_info
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
        '''
        Return the supported PEP 425 tags to check wheel candidates against.
        The tags are returned in order of preference (most preferred first).
        '''
        if self.py_version_info is None:
            py_version_info = sys.version_info[:3]
        else:
            if len(self.py_version_info) < 1 or len(self.py_version_info) > 3:
                raise ValueError("py_version_info must have length 1, 2, or 3")
            py_version_info = self.py_version_info + \
                (3 - len(self.py_version_info)) * (0,)

        if self.implementation is None:
            implementation = sys.implementation.name
        else:
            implementation = self.implementation

        supported_tags = compatible_tags.get_supported(
            version=py_version_info,
            platforms=self.platforms,
            abis=self.abis,
            impl=implementation,
        )
        return sorted(supported_tags, key=lambda tag: (tag.interpreter, tag.abi, tag.platform))

    def get_unsorted_tags(self) -> Set[Tag]:
        '''Exactly the same as get_sorted_tags, but returns a set.
        This is important for performance.
        '''
        return set(self.get_sorted_tags())
