from typing import Optional, List, Tuple, Set
from packaging.tags import Tag, sys_tags, cpython_tags, generic_tags, interpreter_name


class TargetPython:
    '''
    Encapsulates the properties of a Python interpreter one is targeting
    for a package install, download, etc.
    '''

    def __init__(self, platforms: Optional[List[str]] = None, py_version_info: Optional[Tuple[int, ...]] = None,
                 abis: Optional[List[str]] = None, implementation: Optional[str] = None) -> None:
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
        if py_version_info is not None and not (1 <= len(py_version_info) <= 3):
            raise ValueError(
                "py_version_info must be a tuple of length 1, 2, or 3")
        self.platforms = list(platforms) if platforms is not None else None
        self.py_version_info = tuple(
            py_version_info) if py_version_info is not None else None
        self.abis = list(abis) if abis is not None else None
        self.implementation = implementation

        self._sorted_tags_cache: Optional[List[Tag]] = None
        self._unsorted_tags_cache: Optional[Set[Tag]] = None

    def format_given(self) -> str:
        '''
        Format the given, non-None attributes for display.
        '''
        parts: List[str] = []
        if self.platforms is not None:
            parts.append(f"platforms={self.platforms}")
        if self.py_version_info is not None:
            py_ver = ".".join(str(x) for x in self.py_version_info)
            parts.append(f"python_version={py_ver}")
        if self.abis is not None:
            parts.append(f"abis={self.abis}")
        if self.implementation is not None:
            parts.append(f"implementation={self.implementation}")
        return ", ".join(parts)

    def _versions_from_py_version_info(self) -> Optional[List[int]]:
        if not self.py_version_info or len(self.py_version_info) < 2:
            return None
        major, minor = self.py_version_info[0], self.py_version_info[1]
        try:
            version_int = int(f"{major}{minor}")
        except Exception:
            return None
        return [version_int]

    def _interpreter_from_given(self) -> Optional[str]:
        impl = self.implementation or interpreter_name()
        if self.py_version_info is None or len(self.py_version_info) < 2:
            return None
        major, minor = self.py_version_info[0], self.py_version_info[1]
        return f"{impl}{major}{minor}"

    def get_sorted_tags(self) -> List[Tag]:
        '''
        Return the supported PEP 425 tags to check wheel candidates against.
        The tags are returned in order of preference (most preferred first).
        '''
        if self._sorted_tags_cache is not None:
            return list(self._sorted_tags_cache)

        # If nothing specified, use system tags
        if self.platforms is None and self.py_version_info is None and self.implementation is None and self.abis is None:
            tags = list(sys_tags())
            self._sorted_tags_cache = tags
            return list(tags)

        platforms = self.platforms
        abis = self.abis

        # Choose tag generator based on implementation
        impl = (self.implementation or interpreter_name()).lower()

        if impl.startswith("cp"):
            versions = self._versions_from_py_version_info()
            tags_iter = cpython_tags(
                versions=versions, abis=abis, platforms=platforms)
        else:
            interpreter = self._interpreter_from_given()
            tags_iter = generic_tags(
                interpreter=interpreter, abis=abis, platforms=platforms)

        tags_list = list(tags_iter)
        self._sorted_tags_cache = tags_list
        return list(tags_list)

    def get_unsorted_tags(self) -> Set[Tag]:
        '''Exactly the same as get_sorted_tags, but returns a set.
        This is important for performance.
        '''
        if self._unsorted_tags_cache is not None:
            return set(self._unsorted_tags_cache)
        tag_set = set(self.get_sorted_tags())
        self._unsorted_tags_cache = tag_set
        return set(tag_set)
