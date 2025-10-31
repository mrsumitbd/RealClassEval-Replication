
import re
from typing import List, Dict, Iterable

from packaging.tags import Tag as PEP425Tag


class InvalidWheelFilename(ValueError):
    """Raised when a wheel filename does not conform to the expected pattern."""
    pass


class Wheel:
    """A wheel file."""

    _WHEEL_RE = re.compile(
        r"""
        ^(?P<dist>.+?)          # distribution (non-greedy)
        -(?P<ver>.+?)           # version (non-greedy)
        (?:-(?P<build>.+?))?   # optional build tag
        -(?P<py>[^-]+)          # python tag
        -(?P<abi>[^-]+)         # abi tag
        -(?P<plat>[^-]+)        # platform tag
        \.whl$                  # extension
        """,
        re.VERBOSE,
    )

    def __init__(self, filename: str) -> None:
        """
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        """
        m = self._WHEEL_RE.match(filename)
        if not m:
            raise InvalidWheelFilename(f"Invalid wheel filename: {filename!r}")

        self.filename = filename
        self.dist = m.group("dist")
        self.ver = m.group("ver")
        self.build = m.group("build")
        self.py_tag = m.group("py")
        self.abi_tag = m.group("abi")
        self.plat_tag = m.group("plat")

        # Create the list of supported tags for this wheel.
        # A wheel normally supports a single tag combination, but the API
        # is written to handle multiple tag combinations if needed.
        self.file_tags: List[PEP425Tag] = [
            PEP425Tag(self.py_tag, self.abi_tag, self.plat_tag)
        ]

    def get_formatted_file_tags(self) -> List[str]:
        """Return the wheel's tags as a sorted list of strings."""
        tags = [f"{t.python_version}-{t.abi}-{t.platform}" for t in self.file_tags]
        return sorted(tags)

    def support_index_min(self, tags: List[PEP425Tag]) -> int:
        """
        Return the lowest index that one of the wheel's file_tag combinations
        achieves in the given list of supported tags.
        For example, if there are 8 supported tags and one of the file tags
        is first in the list, then return 0.
        :param tags: the PEP 425 tags to check the wheel against, in order
            with most preferred first.
        :raises ValueError: If none of the wheel's file tags match one of
            the supported tags.
        """
        for idx, tag in enumerate(tags):
            if tag in self.file_tags:
                return idx
        raise ValueError("No matching tag found for wheel")

    def find_most_preferred_tag(
        self, tags: List[PEP425Tag], tag_to_priority: Dict[PEP425Tag, int]
    ) -> int:
        """
        Return the priority of the most preferred tag that one of the wheel's file
        tag combinations achieves in the given list of supported tags using the given
        tag_to_priority mapping, where lower priorities are more-preferred.
        This is used in place of support_index_min in some cases in order to avoid
        an expensive linear scan of a large list of tags.
        :param tags: the PEP 425 tags to check the wheel against.
        :param tag_to_priority: a mapping from tag to priority of that tag, where
            lower is more preferred.
        :raises ValueError: If none of the wheel's file tags match one of
            the supported tags.
        """
        best_priority = None
        for tag in tags:
            if tag in self.file_tags:
                priority = tag_to_priority.get(tag)
                if priority is None:
                    continue
                if best_priority is None or priority < best_priority:
                    best_priority = priority
        if best_priority is None:
            raise ValueError("No matching tag found for wheel")
        return best_priority

    def supported(self, tags: Iterable[
