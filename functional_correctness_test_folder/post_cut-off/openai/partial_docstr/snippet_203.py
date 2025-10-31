
from typing import Optional, List, Tuple, Set
from compatibility_tags import get_supported, Tag


class TargetPython:
    def __init__(
        self,
        platforms: Optional[List[str]] = None,
        py_version_info: Optional[Tuple[int, ...]] = None,
        abis: Optional[List[str]] = None,
        implementation: Optional[str] = None,
    ) -> None:
        """
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
        """
        self.platforms = platforms
        self.py_version_info = py_version_info
        self.abis = abis
        self.implementation = implementation

    def format_given(self) -> str:
        """
        Format the given, non-None attributes for display.
        """
        parts = []
        if self.platforms is not None:
            parts.append(f"platforms={self.platforms!r}")
        if self.py_version_info is not None:
            parts.append(f"py_version_info={self.py_version_info!r}")
        if self.abis is not None:
            parts.append(f"abis={self.abis!r}")
        if self.implementation is not None:
            parts.append(f"implementation={self.implementation!r}")
        return ", ".join(parts)

    def get_sorted_tags(self) -> List[Tag]:
        """
        Return a sorted list of tags supported by the target Python configuration.
        Sorting is performed by (python_version, abi, platform) to provide a
        deterministic order.
        """
        tags = get_supported(
            platforms=self.platforms,
            py_version_info=self.py_version_info,
            abis=self.abis,
            implementation=self.implementation,
        )
        # Sort tags by python_version, abi, platform
        return sorted(tags, key=lambda t: (t.python_version, t.abi, t.platform))

    def get_unsorted_tags(self) -> Set[Tag]:
        """
        Exactly the same as get_sorted_tags, but returns a set.
        This is important for performance.
        """
        return set(self.get_sorted_tags())
