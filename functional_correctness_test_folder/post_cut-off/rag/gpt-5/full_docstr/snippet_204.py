from typing import List, Iterable, Dict, FrozenSet
from itertools import product
import os

try:
    from packaging.tags import Tag
except Exception:  # Fallback minimal Tag for typing/runtime if packaging is unavailable
    class Tag:  # type: ignore
        def __init__(self, interpreter: str, abi: str, platform: str) -> None:
            self.interpreter = interpreter
            self.abi = abi
            self.platform = platform

        def __hash__(self) -> int:
            return hash((self.interpreter, self.abi, self.platform))

        def __eq__(self, other: object) -> bool:
            return (
                isinstance(other, Tag)
                and self.interpreter == other.interpreter
                and self.abi == other.abi
                and self.platform == other.platform
            )

        def __str__(self) -> str:
            return f"{self.interpreter}-{self.abi}-{self.platform}"


class Wheel:
    '''A wheel file'''

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        self.filename = filename
        base = os.path.basename(filename)

        if not base.endswith('.whl'):
            raise InvalidWheelFilename(
                f"File does not end with .whl: {filename}")

        stem = base[:-4]
        parts = stem.split('-')
        if len(parts) == 5:
            name, version, py_tag, abi_tag, plat_tag = parts
            build = None
        elif len(parts) == 6:
            name, version, build, py_tag, abi_tag, plat_tag = parts
        else:
            raise InvalidWheelFilename(
                f"Invalid wheel filename (wrong number of parts): {filename}")

        if not all(parts):
            raise InvalidWheelFilename(
                f"Invalid wheel filename (empty component): {filename}")

        # Basic structural validation
        for comp in (py_tag, abi_tag, plat_tag):
            if any(s == '' for s in comp.split('.')):
                raise InvalidWheelFilename(
                    f"Invalid wheel filename (empty tag subcomponent): {filename}")

        self.name = name
        self.version = version
        self.build = build if len(parts) == 6 else None
        self.py_tag = py_tag
        self.abi_tag = abi_tag
        self.plat_tag = plat_tag

        py_tags = py_tag.split('.')
        abi_tags = abi_tag.split('.')
        plat_tags = plat_tag.split('.')

        self.file_tags: FrozenSet[Tag] = frozenset(
            Tag(py, abi, plat) for py, abi, plat in product(py_tags, abi_tags, plat_tags)
        )

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        return sorted(str(t) for t in self.file_tags)

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
        indices = [i for i, t in enumerate(tags) if t in self.file_tags]
        if not indices:
            raise ValueError("Wheel not supported by given tags")
        return min(indices)

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
        priorities = [tag_to_priority[t]
                      for t in self.file_tags if t in tag_to_priority]
        if not priorities:
            raise ValueError("Wheel not supported by given tags")
        return min(priorities)

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        for t in tags:
            if t in self.file_tags:
                return True
        return False
