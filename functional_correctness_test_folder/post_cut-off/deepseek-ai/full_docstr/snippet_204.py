
from typing import List, Dict, Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Tag:
    pass


class InvalidWheelFilename(Exception):
    pass


class Wheel:
    '''A wheel file'''

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        self.filename = filename
        # Validate the filename here (simplified for the example)
        if not filename.endswith('.whl'):
            raise InvalidWheelFilename(f"Invalid wheel filename: {filename}")
        # Parse the tags from the filename (simplified)
        self._file_tags = self._parse_file_tags(filename)

    def _parse_file_tags(self, filename: str) -> List[str]:
        # Simplified parsing logic; actual implementation would parse the wheel filename
        # according to PEP 427.
        parts = filename.split('-')
        if len(parts) < 5:
            raise InvalidWheelFilename(f"Invalid wheel filename: {filename}")
        tags_part = parts[-1].split('.')[:-1]  # Remove the .whl
        return sorted(tags_part)

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        return self._file_tags

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
        file_tags = self.get_formatted_file_tags()
        for i, tag in enumerate(tags):
            if str(tag) in file_tags:
                return i
        raise ValueError("No matching tags found")

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
        file_tags = self.get_formatted_file_tags()
        min_priority = None
        for tag in tags:
            if str(tag) in file_tags:
                priority = tag_to_priority.get(tag, float('inf'))
                if min_priority is None or priority < min_priority:
                    min_priority = priority
        if min_priority is not None:
            return min_priority
        raise ValueError("No matching tags found")

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        file_tags = self.get_formatted_file_tags()
        for tag in tags:
            if str(tag) in file_tags:
                return True
        return False
