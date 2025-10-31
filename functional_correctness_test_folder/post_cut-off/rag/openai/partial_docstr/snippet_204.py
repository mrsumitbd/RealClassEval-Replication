
import re
from typing import List, Dict, Iterable

from packaging.tags import Tag
from packaging.utils import parse_wheel_filename


class InvalidWheelFilename(ValueError):
    """Raised when the wheel filename does not conform to the PEP 427 format."""


class Wheel:
    """A wheel file."""

    def __init__(self, filename: str) -> None:
        """
        Parse a wheel filename and store its PEP 425 tags.

        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        """
        if not filename.endswith(".whl"):
            raise InvalidWheelFilename(
                f"Wheel filename must end with .whl: {filename!r}")

        # Use packaging's helper to parse the filename
        try:
            dist, version, build, py_tag, abi_tag, plat_tag = parse_wheel_filename(
                filename)
        except Exception as exc:
            raise InvalidWheelFilename(
                f"Invalid wheel filename {filename!r}") from exc

        # packaging.parse_wheel_filename returns a tuple where build may be None
        # Build tag is optional; we ignore it for tag generation.
        self.file_tags: List[Tag] = [Tag(py_tag, abi_tag, plat_tag)]

    def get_formatted_file_tags(self) -> List[str]:
        """Return the wheel's tags as a sorted list of strings."""
        return sorted(str(tag) for tag in self.file_tags)

    def support_index_min(self, tags: List[Tag]) -> int:
        """
        Return the lowest index that one of the wheel's file_tag combinations
        achieves in the given list of supported tags.

        :param tags: the PEP 425 tags to check the wheel against, in order
            with most preferred first.
        :raises ValueError: If none of the wheel's file tags match one of
            the supported tags.
        """
        for idx, tag in enumerate(tags):
            if tag in self.file_tags:
                return idx
        raise ValueError("Wheel is not supported by any of the given tags")

    def find_most_preferred_tag(
        self, tags: List[Tag], tag_to_priority: Dict[Tag, int]
    ) -> int:
        """
        Return the priority of the most preferred tag that one of the wheel's file
        tag combinations achieves in the given list of supported tags using the given
        tag_to_priority mapping, where lower priorities are more-preferred.

        :param tags: the PEP 425 tags to check the wheel against.
        :param tag_to_priority: a mapping from tag to priority of that tag, where
            lower is more preferred.
        :raises ValueError: If none of the wheel's file tags match one of
            the supported tags.
        """
        best_priority = None
        for tag in self.file_tags:
            if tag in tags:
                priority = tag_to_priority.get(tag)
                if priority is None:
                    continue
                if best_priority is None or priority < best_priority:
                    best_priority = priority
        if best_priority is None:
            raise ValueError("Wheel is not supported by any of the given tags")
        return best_priority

    def supported(self, tags: Iterable[Tag]) -> bool:
        """Return whether the wheel is compatible with one of the given tags."""
        return any(tag in tags for tag in self.file_tags)
