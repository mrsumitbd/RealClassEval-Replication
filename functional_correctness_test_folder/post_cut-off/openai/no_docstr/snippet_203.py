
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Set, Tuple


@dataclass(frozen=True)
class Tag:
    python_version: str
    abi: str
    platform: str

    def __str__(self) -> str:
        return f"{self.python_version}-{self.abi}-{self.platform}"


class TargetPython:
    """
    Represents a target Python environment for wheel tagging.

    Parameters
    ----------
    platforms : Optional[List[str]]
        List of platform tags (e.g. ['any', 'manylinux1_x86_64']).
    py_version_info : Optional[Tuple[int, ...]]
        Tuple representing the Python version (e.g. (3, 8)).
    abis : Optional[List[str]]
        List of ABI tags (e.g. ['none', 'cp38']).
    implementation : Optional[str]
        Python implementation (e.g. 'cpython', 'pypy').
    """

    def __init__(
        self,
        platforms: Optional[List[str]] = None,
        py_version_info: Optional[Tuple[int, ...]] = None,
        abis: Optional[List[str]] = None,
        implementation: Optional[str] = None,
    ) -> None:
        self.platforms = platforms or ["any"]
        self.py_version_info = py_version_info or (3, 8)
        self.abis = abis or ["none"]
        self.implementation = implementation or "cpython"

        # Normalise python_version string
        self.python_version = self._format_python_version(self.py_version_info)

    @staticmethod
    def _format_python_version(py_version_info: Tuple[int, ...]) -> str:
        """Return the wheel python_version string (e.g. 'py38')."""
        if not py_version_info:
            return "py3"
        major, *rest = py_version_info
        if not rest:
            return f"py{major}"
        minor = rest[0]
        return f"py{major}{minor}"

    def format_given(self) -> str:
        """Return a comma‑separated string of the given tags."""
        tags = self.get_unsorted_tags()
        return ", ".join(sorted(str(tag) for tag in tags))

    def get_sorted_tags(self) -> List[Tag]:
        """Return a list of Tag objects sorted by python_version, abi, platform."""
        tags = self.get_unsorted_tags()
        return sorted(tags, key=lambda t: (t.python_version, t.abi, t.platform))

    def get_unsorted_tags(self) -> Set[Tag]:
        """Return a set of Tag objects for all combinations of the provided lists."""
        tags: Set[Tag] = set()
        for platform in self.platforms:
            for abi in self.abis:
                tags.add(Tag(self.python_version, abi, platform))
        return tags
