
from typing import List, Dict, Iterable


class Wheel:

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.tags = self._parse_tags_from_filename(filename)

    def _parse_tags_from_filename(self, filename: str) -> List[str]:
        # Assuming the tags are separated by hyphens and the version is after the last hyphen
        parts = filename.split('-')
        return parts[1:-1]  # Exclude the package name and version

    def get_formatted_file_tags(self) -> List[str]:
        return self.tags

    def support_index_min(self, tags: List[str]) -> int:
        return min((i for i, tag in enumerate(self.tags) if tag in tags), default=-1)

    def find_most_preferred_tag(self, tags: List[str], tag_to_priority: Dict[str, int]) -> int:
        supported_tags = {tag: tag_to_priority.get(tag, float(
            '-inf')) for tag in self.tags if tag in tag_to_priority}
        if not supported_tags:
            return -1
        most_preferred_tag = max(supported_tags, key=supported_tags.get)
        return self.tags.index(most_preferred_tag)

    def supported(self, tags: Iterable[str]) -> bool:
        return any(tag in self.tags for tag in tags)
