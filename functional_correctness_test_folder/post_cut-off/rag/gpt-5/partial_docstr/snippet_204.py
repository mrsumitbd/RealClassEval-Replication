from __future__ import annotations

import os
from typing import Dict, Iterable, List

from packaging.tags import Tag
from packaging.utils import InvalidWheelFilename, parse_wheel_filename


class Wheel:
    '''A wheel file'''

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        self.filename = filename
        basename = os.path.basename(filename)
        dist, version, build, tags = parse_wheel_filename(basename)
        self.distribution = dist
        self.version = version
        self.build = build
        self.file_tags = frozenset(tags)

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
        tag_to_index = {tag: idx for idx, tag in enumerate(tags)}
        best = None
        for ft in self.file_tags:
            if ft in tag_to_index:
                idx = tag_to_index[ft]
                best = idx if best is None else min(best, idx)
        if best is None:
            raise ValueError("Wheel is not compatible with the given tags.")
        return best

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
        best_priority = None
        for ft in self.file_tags:
            prio = tag_to_priority.get(ft)
            if prio is not None:
                best_priority = prio if best_priority is None else min(
                    best_priority, prio)
        if best_priority is None:
            raise ValueError("Wheel is not compatible with the given tags.")
        return best_priority

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        tag_set = set(tags)
        return any(ft in tag_set for ft in self.file_tags)
