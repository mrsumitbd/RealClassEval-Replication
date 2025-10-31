from typing import Iterable, List, Dict, Set
from packaging.tags import Tag
from packaging.utils import parse_wheel_filename


class Wheel:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        _, _, _, file_tags = parse_wheel_filename(filename)
        self._file_tags: Set[Tag] = set(file_tags)

    def get_formatted_file_tags(self) -> List[str]:
        return sorted(str(t) for t in self._file_tags)

    def support_index_min(self, tags: List[Tag]) -> int:
        tag_to_index: Dict[Tag, int] = {t: i for i, t in enumerate(tags)}
        best = len(tags)
        for t in self._file_tags:
            if t in tag_to_index:
                idx = tag_to_index[t]
                if idx < best:
                    best = idx
                    if best == 0:
                        break
        return best

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        best = len(tags)
        for t in self._file_tags:
            prio = tag_to_priority.get(t)
            if prio is not None and prio < best:
                best = prio
                if best == 0:
                    break
        return best

    def supported(self, tags: Iterable[Tag]) -> bool:
        for t in tags:
            if t in self._file_tags:
                return True
        return False
