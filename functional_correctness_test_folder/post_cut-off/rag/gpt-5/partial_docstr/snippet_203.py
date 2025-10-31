from typing import List, Optional, Set, Tuple
from packaging.tags import Tag, sys_tags, cpython_tags, compatible_tags, generic_tags, interpreter_name


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
        self.platforms = platforms[:] if platforms else None
        self.py_version_info = tuple(
            py_version_info) if py_version_info is not None else None
        self.abis = abis[:] if abis else None
        self.implementation = implementation

    def _versions_param(self) -> Optional[List[str]]:
        if self.py_version_info is None or len(self.py_version_info) == 0:
            return None
        major = self.py_version_info[0]
        minor = self.py_version_info[1] if len(
            self.py_version_info) > 1 else None
        if minor is not None:
            return [f"{major}{minor}"]
        return [f"{major}"]

    def format_given(self) -> str:
        '''
        Format the given, non-None attributes for display.
        '''
        parts: List[str] = []
        if self.platforms:
            parts.append(f"platforms: {', '.join(self.platforms)}")
        if self.py_version_info is not None:
            parts.append("python_version: " + ".".join(str(x)
                         for x in self.py_version_info))
        if self.abis:
            parts.append(f"abis: {', '.join(self.abis)}")
        if self.implementation:
            parts.append(f"implementation: {self.implementation}")
        return "; ".join(parts) if parts else "None"

    def _generate_custom_tags(self) -> List[Tag]:
        vers = self._versions_param()
        plats = self.platforms
        abis = self.abis

        impl = self.implementation or interpreter_name()
        tags: List[Tag] = []

        if impl == "cp":
            tags.extend(
                list(cpython_tags(versions=vers, abis=abis, platforms=plats)))
            tags.extend(list(compatible_tags(versions=vers, platforms=plats)))
            tags.extend(list(generic_tags()))
        else:
            tags.extend(list(compatible_tags(versions=vers, platforms=plats)))
            tags.extend(list(generic_tags()))

        # Deduplicate while preserving order
        seen: Set[Tag] = set()
        unique: List[Tag] = []
        for t in tags:
            if t not in seen:
                seen.add(t)
                unique.append(t)
        return unique

    def get_sorted_tags(self) -> List[Tag]:
        '''
        Return the supported PEP 425 tags to check wheel candidates against.
        The tags are returned in order of preference (most preferred first).
        '''
        if not (self.platforms or self.py_version_info or self.abis or self.implementation):
            return list(sys_tags())
        return self._generate_custom_tags()

    def get_unsorted_tags(self) -> Set[Tag]:
        '''Exactly the same as get_sorted_tags, but returns a set.
        This is important for performance.
        '''
        return set(self.get_sorted_tags())
