
from typing import List, Iterable, Dict
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

    def _parse_filename(self):
        pattern = r'^(.+?)-(\d.+?)(?:-(.+?))?-(.+?)-(?:(?:(.+?)-)?(.+?)-)?(.+?)\.whl$'
        match = re.match(pattern, self.filename)
        if not match:
            raise InvalidWheelFilename(
                f"Invalid wheel filename: {self.filename}")
        name, version, build_tag, python_tag, abi_tag, platform_tag = match.groups()
        return name, version, build_tag, python_tag, abi_tag, platform_tag

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        tags = []
        for python_tag in self.python_tag.split('.'):
            for abi_tag in self.abi_tag.split('.'):
                for platform_tag in self.platform_tag.split('.'):
                    tags.append(f"{python_tag}-{abi_tag}-{platform_tag}")
        return sorted(tags)

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
        for python_tag in self.python_tag.split('.'):
            for abi_tag in self.abi_tag.split('.'):
                for platform_tag in self.platform_tag.split('.'):
                    tag = Tag(python_tag, abi_tag, platform_tag)
                    try:
                        index = tags.index(tag)
                        if index < min_index:
                            min_index = index
                    except ValueError:
                        continue
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
        for python_tag in self.python_tag.split('.'):
            for abi_tag in self.abi_tag.split('.'):
                for platform_tag in self.platform_tag.split('.'):
                    tag = Tag(python_tag, abi_tag, platform_tag)
                    if tag in tag_to_priority:
                        priority = tag_to_priority[tag]
                        if priority < min_priority:
                            min_priority = priority
        if min_priority == float('inf'):
            raise ValueError(
                "None of the wheel's file tags match one of the supported tags.")
        return min_priority

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        for python_tag in self.python_tag.split('.'):
            for abi_tag in self.abi_tag.split('.'):
                for platform_tag in self.platform_tag.split('.'):
                    tag = Tag(python_tag, abi_tag, platform_tag)
                    if tag in tags:
                        return True
        return False
