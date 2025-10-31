
from typing import List, Dict, Iterable


class Tag:
    pass


class Wheel:

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def get_formatted_file_tags(self) -> List[str]:
        formatted_tags = []
        for tag in self.tags:
            formatted_tags.append(f"{tag.name}=={tag.version}")
        return formatted_tags

    def support_index_min(self, tags: List[Tag]) -> int:
        min_index = -1
        for i, tag in enumerate(tags):
            if tag in self.tags:
                min_index = i
                break
        return min_index

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        most_preferred_index = -1
        highest_priority = -1
        for i, tag in enumerate(tags):
            if tag in self.tags and tag_to_priority[tag] > highest_priority:
                highest_priority = tag_to_priority[tag]
                most_preferred_index = i
        return most_preferred_index

    def supported(self, tags: Iterable[Tag]) -> bool:
        for tag in tags:
            if tag not in self.tags:
                return False
        return True
