
from typing import List, Dict, Iterable, Tuple

Tag = Tuple[str, str]


class Wheel:
    def __init__(self, filename: str) -> None:
        # Parse the wheel filename to extract tags
        # Format: {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl
        # Example: mypkg-1.0.0-cp39-cp39-manylinux1_x86_64.whl
        if not filename.endswith('.whl'):
            raise ValueError("Invalid wheel filename")
        name = filename[:-4]
        parts = name.split('-')
        if len(parts) < 5:
            raise ValueError("Invalid wheel filename")
        # The last three parts are python tag, abi tag, platform tag
        self.python_tags = parts[-3].split('.')
        self.abi_tags = parts[-2].split('.')
        self.platform_tags = parts[-1].split('.')
        # Build all supported tags
        self.file_tags: List[Tag] = []
        for py in self.python_tags:
            for abi in self.abi_tags:
                for plat in self.platform_tags:
                    self.file_tags.append((py, abi, plat))

    def get_formatted_file_tags(self) -> List[str]:
        return [f"{py}-{abi}-{plat}" for (py, abi, plat) in self.file_tags]

    def support_index_min(self, tags: List[Tag]) -> int:
        # Return the minimum index in tags where a supported tag is found, or len(tags) if none
        indices = [i for i, tag in enumerate(tags) if tag in self.file_tags]
        return min(indices) if indices else len(tags)

    def find_most_preferred_tag(self, tags: List[Tag], tag_to_priority: Dict[Tag, int]) -> int:
        # Return the index of the supported tag with the lowest priority value
        best_priority = None
        best_index = -1
        for i, tag in enumerate(tags):
            if tag in self.file_tags and tag in tag_to_priority:
                priority = tag_to_priority[tag]
                if best_priority is None or priority < best_priority:
                    best_priority = priority
                    best_index = i
        return best_index

    def supported(self, tags: Iterable[Tag]) -> bool:
        # Return True if any tag in tags is supported
        return any(tag in self.file_tags for tag in tags)
