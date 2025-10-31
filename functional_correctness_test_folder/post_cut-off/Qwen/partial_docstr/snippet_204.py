
from typing import List, Dict, Iterable
from packaging.tags import Tag, parse_tag
import re


class InvalidWheelFilename(Exception):
    pass


class Wheel:
    '''A wheel file'''
    WHEEL_FILE_RE = re.compile(
        r"""^(?P<namever>(?P<name>[^\s-]+)-(?P<version>[^\s-]+))
        ((-(?P<build>\d[^-]*))?-(?P<pyver>[^\s-]+)
        -(?P<abi>[^\s-]+)
        -(?P<plat>[^\s-]+)
        \.whl)$""",
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
        self.tags = list(parse_tag(f"{self.pyver}-{self.abi}-{self.plat}"))

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        return sorted(str(tag) for tag in self.tags)

    def support_index_min(self, tags: List[Tag]) -> int:
        return min((i for i, tag in enumerate(tags) if tag in self.tags), default=-1)

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        supported_tags = {tag: tag_to_priority[tag]
                          for tag in self.tags if tag in tag_to_priority}
        if not supported_tags:
            return -1
        return tags.index(max(supported_tags, key=supported_tags.get))

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        return any(tag in self.tags for tag in tags)
