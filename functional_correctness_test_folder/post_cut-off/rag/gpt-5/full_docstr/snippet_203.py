from typing import List, Optional, Set, Tuple

try:
    from packaging.tags import Tag
except Exception:  # pragma: no cover
    from pip._vendor.packaging.tags import Tag  # type: ignore


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
        if py_version_info is not None and len(py_version_info) not in (1, 2, 3):
            raise ValueError(
                "py_version_info must be a tuple of length 1, 2, or 3")
        self._given_platforms = platforms
        self.py_version_info = py_version_info
        self._given_abis = abis
        self.implementation = implementation

    def format_given(self) -> str:
        '''
        Format the given, non-None attributes for display.
        '''
        parts: List[str] = []
        if self._given_platforms:
            parts.append("platforms: " + ", ".join(self._given_platforms))
        if self.py_version_info is not None:
            parts.append("python_version: " + ".".join(str(p)
                         for p in self.py_version_info))
        if self._given_abis:
            parts.append("abis: " + ", ".join(self._given_abis))
        if self.implementation:
            parts.append("implementation: " + self.implementation)
        return ", ".join(parts) if parts else "None"

    def get_sorted_tags(self) -> List[Tag]:
        '''
        Return the supported PEP 425 tags to check wheel candidates against.
        The tags are returned in order of preference (most preferred first).
        '''
        # Prefer a project-local compatibility_tags if available
        get_supported = None  # type: ignore[assignment]
        try:
            from .compatibility_tags import get_supported as _get_supported  # type: ignore
            get_supported = _get_supported
        except Exception:
            try:
                from compatibility_tags import get_supported as _get_supported  # type: ignore
                get_supported = _get_supported
            except Exception:
                get_supported = None  # type: ignore

        if get_supported is not None:
            try:
                return list(get_supported(  # type: ignore[operator]
                    version=self.py_version_info,
                    platforms=self._given_platforms,
                    abis=self._given_abis,
                    implementation=self.implementation,
                ))
            except TypeError:
                # Fallback for older signature using "impl" instead of "implementation"
                return list(get_supported(  # type: ignore[operator]
                    version=self.py_version_info,
                    platforms=self._given_platforms,
                    abis=self._given_abis,
                    impl=self.implementation,
                ))

        # Final fallback to packaging.tags.sys_tags(), with filtering according to
        # the provided constraints (platforms, abis, implementation, version).
        try:
            from packaging.tags import sys_tags
        except Exception:  # pragma: no cover
            from pip._vendor.packaging.tags import sys_tags  # type: ignore

        tags = list(sys_tags())  # type: List[Tag]

        # Apply filters if constraints are provided.
        if self._given_platforms:
            allowed = set(self._given_platforms)
            tags = [t for t in tags if t.platform in allowed]

        if self._given_abis:
            allowed_abis = set(self._given_abis)
            tags = [t for t in tags if t.abi in allowed_abis]

        if self.implementation:
            impl_prefix = self.implementation
            tags = [t for t in tags if t.interpreter.startswith(impl_prefix)]

        if self.py_version_info is not None:
            # Filter tags whose interpreter indicates a Python version not matching the requested one.
            # We accept tags whose interpreter contains the requested major/minor.
            major = self.py_version_info[0]
            minor = self.py_version_info[1] if len(
                self.py_version_info) >= 2 else None

            def _matches_version(tag: Tag) -> bool:
                interp = tag.interpreter
                # Try to extract integer version suffix from interpreter, e.g. 'cp310' -> (3, 10), 'py39' -> (3, 9), 'py3' -> (3, None)
                digits = "".join(ch for ch in interp if ch.isdigit())
                if not digits:
                    # For interpreters like 'py', assume it's generic and allow it
                    return True
                if len(digits) >= 2:
                    v_major = int(digits[0])
                    v_minor = int(digits[1])
                else:
                    v_major = int(digits[0])
                    v_minor = None
                if v_major != major:
                    return False
                if minor is not None and v_minor is not None and v_minor != minor:
                    return False
                return True

            tags = [t for t in tags if _matches_version(t)]

        return tags

    def get_unsorted_tags(self) -> Set[Tag]:
        '''Exactly the same as get_sorted_tags, but returns a set.
        This is important for performance.
        '''
        return set(self.get_sorted_tags())
