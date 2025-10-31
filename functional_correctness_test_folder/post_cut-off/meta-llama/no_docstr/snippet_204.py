
from typing import List, Dict, Iterable


class Tag:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Wheel:

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.tags = self._parse_filename(filename)

    def _parse_filename(self, filename: str) -> List[Tag]:
        # Assuming filename is in the format 'package-1.0-cp38-cp38-win_amd64.whl'
        # and tags are in the format 'cp38-cp38-win_amd64'
        parts = filename.split('-')
        tag_str = parts[-1].split('.')[0]
        tags = tag_str.split('-')
        python_tag, abi_tag, platform_tag = tags
        return [Tag(f"{python_tag}-{abi_tag}-{platform_tag}")]

    def get_formatted_file_tags(self) -> List[str]:
        return [tag.name for tag in self.tags]

    def support_index_min(self, tags: List[Tag]) -> int:
        try:
            return min([tags.index(tag) for tag in self.tags if tag in tags])
        except ValueError:
            return float('inf')

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        supported_tags = [tag for tag in self.tags if tag in tags]
        if not supported_tags:
            return -1
        most_preferred_tag = max(
            supported_tags, key=lambda tag: tag_to_priority.get(tag, float('-inf')))
        return tags.index(most_preferred_tag)

    def supported(self, tags: Iterable[Tag]) -> bool:
        return any(tag in tags for tag in self.tags)
