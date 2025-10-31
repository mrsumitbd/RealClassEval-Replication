
from typing import List, Dict, Iterable
import re


class Wheel:
    '''A wheel file'''

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        self.filename = filename
        # Parse the wheel filename to extract tags
        match = re.match(
            r'^(?P<namever>.+?)-(?P<pyver>.+?)-(?P<abi>.+?)-(?P<plat>.+?)\.whl$',
            filename
        )
        if not match:
            raise InvalidWheelFilename(f'Invalid wheel filename: {filename}')
        self.file_tags = [
            f'{match.group("pyver")}-{match.group("abi")}-{match.group("plat")}'
        ]

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        return sorted(self.file_tags)

    def support_index_min(self, tags: List[str]) -> int:
        '''Return the lowest index that one of the wheel's file_tag combinations
        achieves in the given list of supported tags.
        For example, if there are 8 supported tags and one of the file tags
        is first in the list, then return 0.
        :param tags: the PEP 425 tags to check the wheel against, in order
            with most preferred first.
        :raises ValueError: If none of the wheel's file tags match one of
            the supported tags.
        '''
        for i, tag in enumerate(tags):
            if tag in self.file_tags:
                return i
        raise ValueError('No matching tags found')

    def find_most_preferred_tag(self, tags: List[str], tag_to_priority: Dict[str, int]) -> int:
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
        for tag in self.file_tags:
            if tag in tag_to_priority:
                priority = tag_to_priority[tag]
                if min_priority is None or priority < min_priority:
                    min_priority = priority
        if min_priority is not None:
            return min_priority
        raise ValueError('No matching tags found')

    def supported(self, tags: Iterable[str]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        return any(tag in self.file_tags for tag in tags)
