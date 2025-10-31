
import re
from typing import List, Dict, Iterable
from packaging.tags import Tag


class InvalidWheelFilename(Exception):
    pass


class Wheel:
    '''A wheel file'''

    WHEEL_INFO_RE = re.compile(
        r"""^(?P<namever>(?P<name>.+?)-(?P<ver>.+?))(-(?P<build>\d[^-]*))?
         -(?P<pyver>.+?)-(?P<abi>.+?)-(?P<plat>.+?)\.whl$""",
        re.VERBOSE
    )

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        self.filename = filename
        wheel_info = self.WHEEL_INFO_RE.match(filename)
        if not wheel_info:
            raise InvalidWheelFilename(
                f"{filename} is not a valid wheel filename.")
        self.name = wheel_info.group('name')
        self.version = wheel_info.group('ver')
        self.build = wheel_info.group('build')
        self.pyver = wheel_info.group('pyver')
        self.abi = wheel_info.group('abi')
        self.plat = wheel_info.group('plat')
        self.file_tags = self._get_file_tags()

    def _get_file_tags(self) -> List[Tag]:
        """Get the tags for a wheel file."""
        # pyver, abi, plat are strings that can contain multiple values separated by '.'
        pyvers = self.pyver.split('.')
        abis = self.abi.split('.')
        plats = self.plat.split('.')
        file_tags = [Tag(pyver, abi, plat)
                     for pyver in pyvers for abi in abis for plat in plats]
        return file_tags

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
        try:
            return min(tags.index(tag) for tag in self.file_tags if tag in tags)
        except ValueError:
            raise ValueError(
                f'None of the wheel\'s file tags ({self.get_formatted_file_tags()}) match one of the supported tags ({[str(tag) for tag in tags]}).')

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
        return min(tag_to_priority[tag] for tag in self.file_tags if tag in tag_to_priority)

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        return any(tag in tags for tag in self.file_tags)
