
import re
from typing import List, Dict, Iterable
from packaging.tags import Tag


class InvalidWheelFilename(Exception):
    pass


class Wheel:
    '''A wheel file'''

    WHEEL_INFO_RE = re.compile(
        r"""^(?P<namever>(?P<name>.+?)-(?P<ver>.*?))
        ((-(?P<build>\d[^-]*?))?-(?P<pyver>.+?)-(?P<abi>.+?)-(?P<plat>.+?)
        \.whl|\.dist-info)$""",
        re.VERBOSE
    )

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        wheel_info = self.WHEEL_INFO_RE.match(filename)
        if not wheel_info:
            raise InvalidWheelFilename(f"Invalid wheel filename: {filename}")
        self.filename = filename
        self.name = wheel_info.group('name')
        self.version = wheel_info.group('ver')
        self.pyver = wheel_info.group('pyver')
        self.abi = wheel_info.group('abi')
        self.plat = wheel_info.group('plat')
        self.file_tags = self._get_file_tags()

    def _get_file_tags(self):
        # This is a simplified version and assumes that the filename is in the correct format.
        # In a real-world scenario, you would need to parse the filename according to PEP 427.
        return [Tag(self.pyver, self.abi, self.plat)]

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        return sorted(f"{tag.interpreter}-{tag.abi}-{tag.platform}" for tag in self.file_tags)

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
        supported_tags = [tag for tag in self.file_tags if tag in tags]
        if not supported_tags:
            raise ValueError(
                "None of the wheel's file tags match one of the supported tags.")
        return min(tag_to_priority[tag] for tag in supported_tags)

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        return any(tag in tags for tag in self.file_tags)
