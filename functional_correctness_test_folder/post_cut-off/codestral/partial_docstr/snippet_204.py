
from typing import List, Dict, Iterable
import re


class InvalidWheelFilename(Exception):
    pass


class Tag:
    def __init__(self, python_tag: str, abi_tag: str, platform_tag: str):
        self.python_tag = python_tag
        self.abi_tag = abi_tag
        self.platform_tag = platform_tag

    def __eq__(self, other):
        if not isinstance(other, Tag):
            return NotImplemented
        return (self.python_tag == other.python_tag and
                self.abi_tag == other.abi_tag and
                self.platform_tag == other.platform_tag)

    def __hash__(self):
        return hash((self.python_tag, self.abi_tag, self.platform_tag))


class Wheel:
    '''A wheel file'''

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        self.filename = filename
        self.name, self.version, self.build_tag, self.python_tag, self.abi_tag, self.platform_tag = self._parse_filename()

    def _parse_filename(self) -> tuple:
        pattern = r'^(.+?)-(\d.+?)-(?:(.+?)-)?(.+?)-(.+?)-(.+?)\.whl$'
        match = re.match(pattern, self.filename)
        if not match:
            raise InvalidWheelFilename(
                f"Invalid wheel filename: {self.filename}")
        return match.groups()

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        tags = [f"{self.python_tag}-{self.abi_tag}-{self.platform_tag}"]
        return sorted(tags)

    def support_index_min(self, tags: List[Tag]) -> int:
        min_index = float('inf')
        for tag in tags:
            if tag.python_tag == self.python_tag and tag.abi_tag == self.abi_tag and tag.platform_tag == self.platform_tag:
                min_index = min(min_index, tags.index(tag))
        return min_index if min_index != float('inf') else -1

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        max_priority = -1
        best_index = -1
        for index, tag in enumerate(tags):
            if tag.python_tag == self.python_tag and tag.abi_tag == self.abi_tag and tag.platform_tag == self.platform_tag:
                priority = tag_to_priority.get(tag, 0)
                if priority > max_priority:
                    max_priority = priority
                    best_index = index
        return best_index

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        for tag in tags:
            if tag.python_tag == self.python_tag and tag.abi_tag == self.abi_tag and tag.platform_tag == self.platform_tag:
                return True
        return False
