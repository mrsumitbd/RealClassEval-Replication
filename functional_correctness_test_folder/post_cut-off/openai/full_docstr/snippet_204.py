
import re
from typing import List, Dict, Iterable

from packaging.tags import Tag


class InvalidWheelFilename(Exception):
    """Raised when a wheel filename does not conform to the PEP 427 format."""
    pass


class Wheel:
    '''A wheel file'''

    _WHEEL_RE = re.compile(
        r"""
        ^(?P<dist>[^-]+)-
        (?P<ver>[^-]+)
        (?:-(?P<build>[^-]+))?-
        (?P<py>[^-]+)-
        (?P<abi>[^-]+)-
        (?P<plat>[^-]+)\.whl$
        """,
        re.VERBOSE,
    )

    def __init__(self, filename: str) -> None:
        """
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        """
        m = self._WHEEL_RE.match(filename)
        if not m:
            raise InvalidWheelFilename(f"Invalid wheel filename: {filename}")

        py_tag = m.group("py")
        abi_tag = m.group("abi")
        plat_tag = m.group("plat")

        # Create a single Tag instance for this wheel
        self._tags: List[Tag] = [Tag(py_tag, abi_tag, plat_tag)]

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        formatted = [
            f"{t.py_tag}-{t.abi_tag}-{t.platform_tag}" for t in self._tags]
        return sorted(formatted)

    def support_index_min(self, tags: List[Tag]) -> int:
        '''Return the lowest index that one of the wheel's file_tag combinations
        achieves in the given list of supported tags.
        For example, if there are 8 supported tags and one of the file tags
        is first in the list, then return 0.
        :param tags: the PEP 425 tags to check the wheel against, in order
            with most preferred first.
        :raises ValueError: If none of the wheel's file tags match one of
            the supported tags.
        '''
        min_index = None
        for idx, tag in enumerate(tags):
            if tag in self._tags:
                min_index = idx
                break
        if min_index is None:
            raise ValueError(
                "Wheel is not compatible with any of the provided tags")
        return min_index

    def find_most_preferred_tag(
        self, tags: List[Tag], tag_to_priority: Dict[Tag, int]
    ) -> int:
        '''Return the priority of the most preferred tag that one of the wheel's file
        tag combinations achieves in the given list of supported tags using the given
        tag_to_priority mapping, where lower priorities are more-preferred.
        This is used in place of support_index_min in some cases in order to avoid
        an expensive linear scan of a large list of tags.
        :param tags: the PEP 425 tags to check the wheel against.
        :param tag_to_priority: a mapping from tag to priority of that tag, where
            lower is more preferred.
        :raises ValueError: If none of the wheel's file tags match one of
            the supported tags.
        '''
        min_priority = None
        for tag in self._tags:
            if tag in tag_to_priority:
                priority = tag_to_priority[tag]
                if min_priority is None or priority < min_priority:
                    min_priority = priority
        if min_priority is None:
            raise ValueError(
                "Wheel is not compatible with any of the provided tags")
        return min_priority

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        return any(tag in self._tags for tag in tags)
