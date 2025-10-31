
from packaging.tags import Tag
from packaging.wheel import WheelFileName
from typing import List, Iterable, Dict


class InvalidWheelFilename(Exception):
    pass


class Wheel:
    '''A wheel file'''

    def __init__(self, filename: str) -> None:
        '''
        :raises InvalidWheelFilename: when the filename is invalid for a wheel
        '''
        try:
            self.wheel_info = WheelFileName(filename)
        except ValueError:
            raise InvalidWheelFilename(
                f"'{filename}' is not a valid wheel filename")

    def get_formatted_file_tags(self) -> List[str]:
        '''Return the wheel's tags as a sorted list of strings.'''
        return sorted(f"{tag}" for tag in self.wheel_info.tags)

    def support_index_min(self, tags: List[Tag]) -> int:
        min_index = float('inf')
        for tag in self.wheel_info.tags:
            try:
                min_index = min(min_index, tags.index(tag))
            except ValueError:
                continue
        return min_index if min_index != float('inf') else -1

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        best_priority = float('-inf')
        best_index = -1
        for i, tag in enumerate(tags):
            if tag in self.wheel_info.tags:
                priority = tag_to_priority.get(tag, float('-inf'))
                if priority > best_priority:
                    best_priority = priority
                    best_index = i
        return best_index

    def supported(self, tags: Iterable[Tag]) -> bool:
        '''Return whether the wheel is compatible with one of the given tags.
        :param tags: the PEP 425 tags to check the wheel against.
        '''
        return any(tag in self.wheel_info.tags for tag in tags)
