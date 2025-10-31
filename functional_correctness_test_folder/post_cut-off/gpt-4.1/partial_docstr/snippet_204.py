
import re
from typing import List, Dict, Iterable, Tuple


class InvalidWheelFilename(Exception):
    pass


class Tag:
    def __init__(self, interpreter: str, abi: str, platform: str):
        self.interpreter = interpreter
        self.abi = abi
        self.platform = platform

    def __eq__(self, other):
        if not isinstance(other, Tag):
            return False
        return (self.interpreter, self.abi, self.platform) == (other.interpreter, other.abi, other.platform)

    def __hash__(self):
        return hash((self.interpreter, self.abi, self.platform))

    def __str__(self):
        return f"{self.interpreter}-{self.abi}-{self.platform}"

    def __repr__(self):
        return f"Tag({self.interpreter!r}, {self.abi!r}, {self.platform!r})"


class Wheel:
    '''A wheel file'''
    WHEEL_FILENAME_RE = re.compile(
        r"""^(?P<namever>(?P<name>.+?)-(?P<ver>.+?))
        (-(?P<build>\d[^-]*))?
        -(?P<pyver>[^-]+)
        -(?P<abi>[^-]+)
        -(?P<plat>[^-]+)
        \.whl$""",
        re.VERBOSE
    )

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        m = self.WHEEL_FILENAME_RE.match(filename)
        if not m:
            raise InvalidWheelFilename(f"Invalid wheel filename: {filename}")
        self.filename = filename
        self.name = m.group('name')
        self.version = m.group('ver')
        self.build = m.group('build')
        self.pyver = m.group('pyver')
        self.abi = m.group('abi')
        self.plat = m.group('plat')
        # tags are all combinations of pyver, abi, plat (PEP 427)
        self.file_tags = []
        for py in self.pyver.split('.'):
            for abi in self.abi.split('.'):
                for plat in self.plat.split('.'):
                    self.file_tags.append(Tag(py, abi, plat))

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        tags = [str(tag) for tag in self.file_tags]
        return sorted(tags)

    def support_index_min(self, tags: List[Tag]) -> int:
        # Return the lowest index in tags that matches a file_tag, or len(tags) if none
        for idx, tag in enumerate(tags):
            if tag in self.file_tags:
                return idx
        return len(tags)

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        # Return the lowest priority value among matching tags, or len(tags) if none
        min_priority = len(tags)
        for tag in self.file_tags:
            if tag in tag_to_priority:
                min_priority = min(min_priority, tag_to_priority[tag])
        return min_priority

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        file_tag_set = set(self.file_tags)
        for tag in tags:
            if tag in file_tag_set:
                return True
        return False
