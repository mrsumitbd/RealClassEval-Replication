
from typing import List
import os


class ContentMixin:

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        base_path = os.path.join('content', sub_folder)
        files = []
        for ext in extensions:
            files.extend([f for f in os.listdir(base_path) if f.endswith(ext)])
        return files

    def list_available_worlds(self) -> List[str]:
        return self._list_content_files('worlds', ['.world', '.json'])

    def list_available_addons(self) -> List[str]:
        return self._list_content_files('addons', ['.addon', '.mod'])
