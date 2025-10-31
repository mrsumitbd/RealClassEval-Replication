
from packaging.tags import Tag
from packaging.utils import parse_wheel_filename
from typing import List, Dict, Iterable


class InvalidWheelFilename(Exception):
    pass


class Wheel:
    '''A wheel file'''

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        try:
            self.name, self.version, self.build, self.tags = parse_wheel_filename(
                filename)
        except Exception as e:
            raise InvalidWheelFilename(
                f"Invalid wheel filename: {filename}") from e

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        return sorted([str(tag) for tag in self.tags])

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
        min_index = float('inf')
        for tag in self.tags:
            try:
                index = tags.index(tag)
                min_index = min(min_index, index)
            except ValueError:
                pass
        if min_index == float('inf'):
            raise ValueError(
                "None of the wheel's file tags match one of the supported tags.")
        return min_index

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
        for tag in self.tags:
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
        return any(tag in tags for tag in self.tags)
