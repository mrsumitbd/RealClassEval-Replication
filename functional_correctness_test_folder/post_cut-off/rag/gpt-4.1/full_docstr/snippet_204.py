
import re
from typing import List, Dict, Iterable


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
        r"""^(?P<distribution>[^-]+)
        (?:-(?P<version>[^-]+))
        (?:-(?P<build_tag>[^-]+))?
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
        self.filename = filename
        m = self.WHEEL_FILENAME_RE.match(filename)
        if not m:
            raise InvalidWheelFilename(f"Invalid wheel filename: {filename}")
        self.distribution = m.group("distribution")
        self.version = m.group("version")
        self.build_tag = m.group("build_tag")
        self.python_tag = m.group("python_tag")
        self.abi_tag = m.group("abi_tag")
        self.platform_tag = m.group("platform_tag")
        self.file_tags = self._generate_file_tags()

    def _generate_file_tags(self) -> List[Tag]:
        python_tags = self.python_tag.split('.')
        abi_tags = self.abi_tag.split('.')
        platform_tags = self.platform_tag.split('.')
        tags = []
        for interpreter in python_tags:
            for abi in abi_tags:
                for platform in platform_tags:
                    tags.append(Tag(interpreter, abi, platform))
        return tags

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        return sorted(str(tag) for tag in self.file_tags)

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
        tag_set = set(self.file_tags)
        for idx, tag in enumerate(tags):
            if tag in tag_set:
                return idx
        raise ValueError("Wheel is not compatible with any supported tags.")

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
        priorities = [
            tag_to_priority[tag]
            for tag in self.file_tags
            if tag in tag_to_priority
        ]
        if not priorities:
            raise ValueError(
                "Wheel is not compatible with any supported tags.")
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
