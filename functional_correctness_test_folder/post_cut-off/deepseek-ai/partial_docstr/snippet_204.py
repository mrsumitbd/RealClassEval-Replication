
from typing import List, Dict, Iterable
from dataclasses import dataclass


@dataclass
class Tag:
    interpreter: str
    abi: str
    platform: str


class InvalidWheelFilename(Exception):
    pass


class Wheel:
    '''A wheel file'''

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        if not filename.endswith('.whl'):
            raise InvalidWheelFilename(
                "Invalid wheel filename: must end with .whl")

        parts = filename.split('-')
        if len(parts) < 5:
            raise InvalidWheelFilename(
                "Invalid wheel filename: insufficient parts")

        self._filename = filename
        self._tags = self._parse_tags(parts[-1])

    def _parse_tags(self, tag_part: str) -> List[Tag]:
        tags = []
        for tag in tag_part.split('.'):
            if '-' in tag:
                interpreter, abi, platform = tag.split('-')
                tags.append(Tag(interpreter, abi, platform))
        return tags

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        formatted_tags = [
            f"{tag.interpreter}-{tag.abi}-{tag.platform}"
            for tag in self._tags
        ]
        return sorted(formatted_tags)

    def support_index_min(self, tags: List[Tag]) -> int:
        for i, tag in enumerate(tags):
            if tag in self._tags:
                return i
        return -1

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        min_priority = float('inf')
        result_index = -1

        for i, tag in enumerate(tags):
            if tag in self._tags:
                priority = tag_to_priority.get(tag, float('inf'))
                if priority < min_priority:
                    min_priority = priority
                    result_index = i
        return result_index

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        return any(tag in self._tags for tag in tags)
