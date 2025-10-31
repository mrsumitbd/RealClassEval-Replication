from typing import Optional, List, Tuple, Set
import sys

try:
    from packaging.tags import (
        Tag,
        sys_tags,
        cpython_tags,
        generic_tags,
        compatible_tags,
        interpreter_name,
        interpreter_version,
    )
except Exception:  # Fallback if packaging isn't available; define minimal Tag for typing
    class Tag:  # type: ignore
        def __init__(self, interpreter: str, abi: str, platform: str) -> None:
            self.interpreter = interpreter
            self.abi = abi
            self.platform = platform

        def __hash__(self) -> int:
            return hash((self.interpreter, self.abi, self.platform))

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Tag):
                return NotImplemented
            return (
                self.interpreter == other.interpreter
                and self.abi == other.abi
                and self.platform == other.platform
            )


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
        if py_version_info is not None:
            if not (1 <= len(py_version_info) <= 3):
                raise ValueError(
                    "py_version_info must be a tuple of length 1, 2, or 3 when provided.")
            # Normalize to ints
            py_version_info = tuple(int(v) for v in py_version_info)

        self.platforms: Optional[List[str]
                                 ] = platforms[:] if platforms else None
        self.py_version_info: Optional[Tuple[int, ...]] = py_version_info
        self.abis: Optional[List[str]] = abis[:] if abis else None
        self.implementation: Optional[str] = implementation

    def format_given(self) -> str:
        '''
        Format the given, non-None attributes for display.
        '''
        parts: List[str] = []
        if self.platforms:
            parts.append("platforms=" + ",".join(self.platforms))
        if self.abis:
            parts.append("abis=" + ",".join(self.abis))
        if self.implementation:
            parts.append("implementation=" + self.implementation)
        if self.py_version_info:
            parts.append("python_version=" + ".".join(str(x)
                         for x in self.py_version_info))
        return ", ".join(parts)

    def get_sorted_tags(self) -> List[Tag]:
        '''
        Return the supported PEP 425 tags to check wheel candidates against.
        The tags are returned in order of preference (most preferred first).
        '''
        # If no overrides are provided, rely on the environment's sys_tags ordering.
        if (
            self.platforms is None
            and self.py_version_info is None
            and self.abis is None
            and self.implementation is None
        ):
            try:
                return list(sys_tags())
            except NameError:
                return []

        # Prepare parameters
        platforms = self.platforms
        abis = self.abis
        impl = self.implementation

        # Determine (major, minor) for tag generation if provided
        py_ver_tuple = None  # type: Optional[Tuple[int, int]]
        if self.py_version_info is not None:
            major = self.py_version_info[0]
            minor = self.py_version_info[1] if len(
                self.py_version_info) >= 2 else sys.version_info.minor
            py_ver_tuple = (major, minor)

        # Determine interpreter information
        try:
            current_impl = impl if impl is not None else interpreter_name()
            ver_str = interpreter_version(py_ver_tuple)  # e.g. '311'
        except NameError:
            current_impl = impl if impl is not None else "cp"
            ver_str = f"{py_ver_tuple[0]}{py_ver_tuple[1]}" if py_ver_tuple else ""

        interpreter_str = (
            current_impl + ver_str) if current_impl and ver_str else None

        tags: List[Tag] = []

        # Primary tags based on implementation
        used_primary = False
        try:
            if current_impl == "cp":
                tags.extend(cpython_tags(py_version=py_ver_tuple,
                            abis=abis, platforms=platforms))
                used_primary = True
            else:
                tags.extend(generic_tags(py_version=py_ver_tuple, abis=abis,
                            platforms=platforms, interpreter=interpreter_str))
                used_primary = True
        except NameError:
            # packaging not available; cannot generate sophisticated tags
            used_primary = False

        # Fallback if primary generation failed and no sys_tags already
        if not used_primary:
            try:
                tags.extend(sys_tags())
            except NameError:
                pass

        # Add compatibility tags for broader matches
        try:
            compat = list(compatible_tags(py_version=py_ver_tuple,
                          platforms=platforms, interpreter=interpreter_str))
            # Preserve ordering and avoid duplicates
            existing = set(tags)
            for t in compat:
                if t not in existing:
                    tags.append(t)
        except NameError:
            pass

        return tags

    def get_unsorted_tags(self) -> Set[Tag]:
        '''Exactly the same as get_sorted_tags, but returns a set.
        This is important for performance.
        '''
        return set(self.get_sorted_tags())
