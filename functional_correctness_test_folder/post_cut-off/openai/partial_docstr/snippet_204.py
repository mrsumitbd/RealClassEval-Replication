
from __future__ import annotations

import os
from typing import Dict, Iterable, List, Optional

from packaging.tags import Tag


class InvalidWheelFilename(ValueError):
    """Raised when the wheel filename is not valid."""
    pass


class Wheel:
    """A wheel file."""

    def __init__(self, filename: str) -> None:
        """
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        """
        if not filename.endswith(".whl"):
            raise InvalidWheelFilename(
                f"Wheel filename must end with .whl: {filename}")

        # Strip the .whl suffix
        base = filename[:-4]

        # Split off the last three tags: python_tag-abi_tag-platform_tag
        try:
            parts, py_tag, abi_tag, plat_tag = base.rsplit("-", 3)
        except ValueError:
            raise InvalidWheelFilename(
                f"Wheel filename does not contain enough parts: {filename}")

        # Now split the remaining part into distribution, version, optional build tag
        dist_ver_parts = parts.rsplit("-", 2)
        if len(dist_ver_parts) == 3:
            distribution, version, build_tag = dist_ver_parts
        elif len(dist_ver_parts) == 2:
            distribution, version = dist_ver_parts
            build_tag = None
        else:
            raise InvalidWheelFilename(
                f"Wheel filename does not contain distribution and version: {filename}")

        # Validate that distribution and version are non-empty
        if not distribution or not version:
            raise InvalidWheelFilename(
                f"Distribution or version missing in wheel filename: {filename}")

        # Validate tags by attempting to construct a Tag object
        try:
            tag = Tag(py_tag, abi_tag, plat_tag)
        except Exception as exc:
            raise InvalidWheelFilename(
                f"Invalid tags in wheel filename: {filename}") from exc

        self.filename = filename
        self.distribution = distribution
        self.version = version
        self.build_tag = build_tag
        self.python_tag = py_tag
        self.abi_tag = abi_tag
        self.platform_tag = plat_tag
        self.tag = tag

    def get_formatted_file_tags(self) -> List[str]:
        """Return the wheel's tags as a sorted list of strings."""
        return [str(self.tag)]

    def support_index_min(self, tags: List[Tag]) -> int:
        """
        Return the index of the first tag in `tags` that is supported by this wheel.
        If none are supported, return len(tags).
        """
        for idx, t in enumerate(tags):
            if t == self.tag:
                return idx
        return len(tags)

    def find_most_preferred_tag(
        self, tags: List[Tag], tag_to_priority: Dict[Tag, int]
    ) -> int:
        """
        Return the index of the most preferred supported tag.
        Preference is determined by the lowest priority value in `tag_to_priority`.
        If no supported tag is found, return len(tags).
        """
        best_idx = len(tags)
        best_priority: Optional[int] = None
