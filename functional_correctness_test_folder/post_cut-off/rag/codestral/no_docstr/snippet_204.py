
from typing import List, Dict, Iterable
import re


class Wheel:
    '''A wheel file'''

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        self.filename = filename
        self.name, self.version, self.build_tag, self.python_tag, self.abi_tag, self.platform_tag = self._parse_filename()

    def _parse_filename(self) -> tuple:
        '''Parse the wheel filename into its components.'''
        pattern = r'^(.+?)-(\d.+?)-(?:(.+?)-)?(.+?)-(.+?)\.whl$'
        match = re.match(pattern, self.filename)
        if not match:
            raise InvalidWheelFilename(
                f"Invalid wheel filename: {self.filename}")
        name, version, build_tag, python_tag, abi_tag, platform_tag = match.groups()
        return name, version, build_tag, python_tag, abi_tag, platform_tag

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        tags = [
            f"{self.python_tag}-{self.abi_tag}-{self.platform_tag}",
            f"{self.python_tag}-none-{self.platform_tag}",
            f"py2.py3-none-{self.platform_tag}",
            f"py2-none-{self.platform_tag}",
            f"py3-none-{self.platform_tag}",
            f"py2.py3-none-any",
            f"py2-none-any",
            f"py3-none-any",
            f"none-any"
        ]
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
        file_tags = self.get_formatted_file_tags()
        for tag in tags:
            if tag in file_tags:
                return tags.index(tag)
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
        file_tags = self.get_formatted_file_tags()
        min_priority = None
        for tag in tags:
            if tag in file_tags:
                priority = tag_to_priority.get(tag, float('inf'))
                if min_priority is None or priority < min_priority:
                    min_priority = priority
        if min_priority is not None:
            return min_priority
        raise ValueError(
            "None of the wheel's file tags match one of the supported tags.")

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        file_tags = self.get_formatted_file_tags()
        for tag in tags:
            if tag in file_tags:
                return True
        return False


class InvalidWheelFilename(Exception):
    '''Raised when the wheel filename is invalid.'''
    pass
