
import re
from typing import List, Dict, Iterable, Tuple


class InvalidWheelFilename(Exception):
    pass


class Tag:
    """
    Represents a PEP 425 tag as a tuple: (interpreter, abi, platform)
    """

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

    def __repr__(self):
        return f"{self.interpreter}-{self.abi}-{self.platform}"

    def __str__(self):
        return f"{self.interpreter}-{self.abi}-{self.platform}"


class Wheel:
    '''A wheel file'''

    WHEEL_FILENAME_RE = re.compile(
        r"""^(?P<distribution>.+?)-(?P<version>.+?)
        (-(?P<build>\d[^-]*))?
        -(?P<python_tag>[^-]+)
        -(?P<abi_tag>[^-]+)
        -(?P<platform_tag>[^-]+)
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
        self.distribution = m.group("distribution")
        self.version = m.group("version")
        self.build = m.group("build")
        self.python_tag = m.group("python_tag")
        self.abi_tag = m.group("abi_tag")
        self.platform_tag = m.group("platform_tag")
        # Compute all file tags (as Tag objects)
        self.file_tags = []
        for py in self.python_tag.split('.'):
            for abi in self.abi_tag.split('.'):
                for plat in self.platform_tag.split('.'):
                    self.file_tags.append(Tag(py, abi, plat))

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        tags = [str(tag) for tag in self.file_tags]
        return sorted(tags)

    def support_index_min(self, tags: List[Tag]) -> int:
        '''Return the lowest index that one of the wheel's file_tag combinations
        achieves in the given list of supported tags.
        :param tags: the PEP 425 tags to check the wheel against, in order
            with most preferred first.
        :raises ValueError: If none of the wheel's file tags match one of
            the supported tags.
        '''
        tag_set = set(self.file_tags)
        for idx, tag in enumerate(tags):
            if tag in tag_set:
                return idx
        raise ValueError(
            "None of the wheel's file tags match the supported tags.")

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        '''Return the priority of the most preferred tag that one of the wheel's file
        tag combinations achieves in the given list of supported tags using the given
        tag_to_priority mapping, where lower priorities are more-preferred.
        :param tags: the PEP 425 tags to check the wheel against.
        :param tag_to_priority: a mapping from tag to priority of that tag, where
            lower is more preferred.
        :raises ValueError: If none of the wheel's file tags match one of
            the supported tags.
        '''
        priorities = []
        for tag in self.file_tags:
            if tag in tag_to_priority:
                priorities.append(tag_to_priority[tag])
        if not priorities:
            raise ValueError(
                "None of the wheel's file tags match the supported tags.")
        return min(priorities)

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        tag_set = set(self.file_tags)
        for tag in tags:
            if tag in tag_set:
                return True
        return False
