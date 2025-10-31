from typing import List, Iterable, Dict, Set
from packaging.tags import Tag
from packaging.utils import parse_wheel_filename


class Wheel:
    '''A wheel file'''

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        self.filename = filename
        try:
            self.name, self.version, self.build_tag, file_tags = parse_wheel_filename(
                filename)
        except Exception as e:
            # Re-raise as the expected InvalidWheelFilename from the caller's context
            raise InvalidWheelFilename(str(e))  # type: ignore[name-defined]
        self.file_tags: Set[Tag] = set(file_tags)

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
        for idx, tag in enumerate(tags):
            if tag in self.file_tags:
                return idx
        raise ValueError("Wheel is not compatible with the given tags")

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
        tag_set = set(tags)
        candidates = (
            t for t in self.file_tags if t in tag_set and t in tag_to_priority)
        best = None
        for t in candidates:
            prio = tag_to_priority[t]
            if best is None or prio < best:
                best = prio
        if best is None:
            raise ValueError("Wheel is not compatible with the given tags")
        return best

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        return any(t in self.file_tags for t in tags)
