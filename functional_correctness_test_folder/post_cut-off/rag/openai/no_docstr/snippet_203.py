
from __future__ import annotations

from typing import List, Optional, Sequence, Set, Tuple
import sys

# Import the tags module from importlib.metadata (Python 3.10+)
try:
    from importlib.metadata import tags as _tags_module
except Exception:  # pragma: no cover
    # Fallback for older Python versions that provide the same API
    from importlib_metadata import tags as _tags_module

Tag = _tags_module.Tag  # type: ignore


class TargetPython:
    """
    Encapsulates the properties of a Python interpreter one is targeting
    for a package install, download, etc.
    """

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
        parts: List[str] = []
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
        Return the supported PEP 425 tags to check wheel candidates against.
        The tags are returned in order of preference (most preferred first).
        """
        # Determine the version tuple to use
        version = self.py_version_info
        if version is None:
            # Use the current interpreter's version info (major, minor, micro)
            version = sys.version_info[:3]

        # Retrieve tags from importlib.metadata.tags
        tags = _tags_module.get_supported(
            abis=self.abis,
            implementation=self.implementation,
            version=version,
        )

        # Filter by platforms if specified
        if self.platforms is not None:
            tags = [t for t in tags if t.platform in self.platforms]

        return list(tags)

    def get_unsorted_tags(self) -> Set[Tag]:
        """
        Exactly the same as get_sorted_tags, but returns a set.
        This is important for performance.
        """
        return set(self.get_sorted_tags())
