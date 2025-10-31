from typing import List, Optional, Set, Tuple

try:
    from packaging.tags import Tag
except Exception:  # Fallback type stub if packaging is unavailable at runtime
    class Tag:  # type: ignore
        def __init__(self, *args, **kwargs) -> None:
            pass

try:
    # Expected to be available in the environment using this class
    from compatibility_tags import get_supported
except Exception:
    # Provide a clear error at call time if not available
    def get_supported(*args, **kwargs):  # type: ignore
        raise RuntimeError(
            "compatibility_tags.get_supported is required but not available.")


class TargetPython:
    def __init__(
        self,
        platforms: Optional[List[str]] = None,
        py_version_info: Optional[Tuple[int, ...]] = None,
        abis: Optional[List[str]] = None,
        implementation: Optional[str] = None,
    ) -> None:
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
                raise ValueError("py_version_info must have length 1, 2, or 3")
            if not all(isinstance(x, int) and x >= 0 for x in py_version_info):
                raise ValueError(
                    "py_version_info must be a tuple of non-negative ints")
        if platforms is not None:
            if not isinstance(platforms, list) or not all(isinstance(p, str) for p in platforms):
                raise ValueError("platforms must be a list of strings or None")
        if abis is not None:
            if not isinstance(abis, list) or not all(isinstance(a, str) for a in abis):
                raise ValueError("abis must be a list of strings or None")
        if implementation is not None and not isinstance(implementation, str):
            raise ValueError("implementation must be a string or None")

        self._platforms = platforms
        self._py_version_info = py_version_info
        self._abis = abis
        self._implementation = implementation

    def format_given(self) -> str:
        '''
        Format the given, non-None attributes for display.
        '''
        parts: List[str] = []
        if self._platforms is not None:
            parts.append(f"platforms={self._platforms!r}")
        if self._py_version_info is not None:
            parts.append(f"py_version_info={self._py_version_info!r}")
        if self._abis is not None:
            parts.append(f"abis={self._abis!r}")
        if self._implementation is not None:
            parts.append(f"implementation={self._implementation!r}")
        return ", ".join(parts) if parts else "(none)"

    def _compute_versions(self) -> Optional[List[str]]:
        pvi = self._py_version_info
        if pvi is None:
            return None
        if len(pvi) == 1:
            return [str(pvi[0])]
        # Use major and minor for version strings, ignoring micro
        major, minor = pvi[0], pvi[1]
        return [f"{major}{minor}"]

    def get_sorted_tags(self) -> List[Tag]:
        versions = self._compute_versions()
        return list(
            get_supported(
                versions=versions,
                platforms=self._platforms,
                impl=self._implementation,
                abis=self._abis,
            )
        )

    def get_unsorted_tags(self) -> Set[Tag]:
        '''Exactly the same as get_sorted_tags, but returns a set.
        This is important for performance.
        '''
        return set(self.get_sorted_tags())
