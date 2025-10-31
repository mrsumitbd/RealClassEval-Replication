
from __future__ import annotations

from typing import List, Optional, Set, Tuple
import sys

# Import the tags module from importlib.metadata (Python 3.8+)
try:
    from importlib.metadata import tags as _tags
except Exception:  # pragma: no cover
    # Fallback for older Python versions that may not have importlib.metadata
    from importlib_metadata import tags as _tags  # type: ignore

Tag = Tuple[str, str, str]


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

        return ", ".join(parts) if parts else "None"

    def _get_python_version_str(self) -> Optional[str]:
        if self.py_version_info is None:
            return None
        # Convert tuple to string like "3.8" or "3.8.5"
        return ".".join(str(v) for v in self.py_version_info)

    def get_sorted_tags(self) -> List[Tag]:
        """
        Return the supported PEP 425 tags to check wheel candidates against.
        The tags are returned in order of preference (most preferred first).
        """
        python_version = self._get_python_version_str()
        # get_supported returns a list of Tag tuples sorted by preference
        tags = _tags.get_supported(
            abis=self.abis,
            implementation=self.implementation,
            python_version=python_version,
        )
        if self.platforms is None:
            return tags

        # Filter tags by platform
        platform_set = set(self.platforms)
        filtered = [t for t in tags if t[2] in platform_set]
        return filtered

    def get_unsorted_tags(self) -> Set[Tag]:
        """
        Exactly the same as get_sorted_tags, but returns a set.
        This is important for performance.
        """
        return set(self.get_sorted_tags())
