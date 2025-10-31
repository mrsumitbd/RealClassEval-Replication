
from typing import List, Dict, Iterable
from typing import TypeVar, Generic

Tag = TypeVar('Tag')


class Wheel:

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def get_formatted_file_tags(self) -> List[str]:
        return []

    def support_index_min(self, tags: List[Tag]) -> int:
        return -1

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        return -1

    def supported(self, tags: Iterable[Tag]) -> bool:
        return False
