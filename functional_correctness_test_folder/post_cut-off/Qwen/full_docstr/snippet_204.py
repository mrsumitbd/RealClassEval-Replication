
import re
from typing import List, Dict, Iterable
from packaging.tags import Tag, parse_tag


class InvalidWheelFilename(Exception):
    pass


class Wheel:
    '''A wheel file'''

    WHEEL_FILE_RE = re.compile(
        r"""^(?P<namever>(?P<name>[^\s-]+)-(?P<version>[^\s-]+))
        ((-(?P<build>\d[^-]*))?-(?P<pyver>[^\s-]+)-(?P<abi>[^\s-]+)-(?P<plat>[^\s-]+)\.whl)$""",
        re.VERBOSE
    )

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        match = self.WHEEL_FILE_RE.match(filename)
        if not match:
            raise InvalidWheelFilename(f"Invalid wheel filename: {filename}")
        self.filename = filename
        self.name = match.group('name')
        self.version = match.group('version')
        self.build = match.group('build')
        self.pyver = match.group('pyver')
        self.abi = match.group('abi')
        self.plat = match.group('plat')
        self.file_tags = [Tag(self.pyver, self.abi, self.plat)]

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        return sorted(str(tag) for tag in self.file_tags)

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
        for index, tag in enumerate(tags):
            if tag in self.file_tags:
                return index
        raise ValueError(
            "None of the wheel's file tags match one of the supported tags.")

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
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
        min_priority = float('inf')
        for tag in self.file_tags:
            if tag in tag_to_priority:
                min_priority = min(min_priority, tag_to_priority[tag])
        if min_priority == float('inf'):
            raise ValueError(
                "None of the wheel's file tags match one of the supported tags.")
        return min_priority

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        return any(tag in self.file_tags for tag in tags)
