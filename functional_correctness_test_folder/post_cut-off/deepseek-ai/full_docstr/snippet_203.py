
from typing import Optional, List, Tuple, Set
from packaging.tags import Tag


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
        parts = []
        if self.platforms is not None:
            parts.append(f"platforms={self.platforms}")
        if self.py_version_info is not None:
            parts.append(f"version_info={self.py_version_info}")
        if self.abis is not None:
            parts.append(f"abis={self.abis}")
        if self.implementation is not None:
            parts.append(f"implementation={self.implementation}")
        return ", ".join(parts)

    def get_sorted_tags(self) -> List[Tag]:
        '''
        Return the supported PEP 425 tags to check wheel candidates against.
        The tags are returned in order of preference (most preferred first).
        '''
        from packaging.tags import sys_tags
        if self.py_version_info is None and self.abis is None and self.implementation is None:
            return list(sys_tags())
        else:
            from packaging.tags import interpreter_name, interpreter_version
            impl = self.implementation if self.implementation is not None else interpreter_name()
            version = self.py_version_info if self.py_version_info is not None else interpreter_version()
            abis = self.abis if self.abis is not None else None
            platforms = self.platforms if self.platforms is not None else None
            from packaging.tags import _get_sys_tags
            tags = _get_sys_tags(
                interpreter=impl, version_info=version, abis=abis, platforms=platforms)
            return list(tags)

    def get_unsorted_tags(self) -> Set[Tag]:
        '''Exactly the same as get_sorted_tags, but returns a set.
        This is important for performance.
        '''
        return set(self.get_sorted_tags())
