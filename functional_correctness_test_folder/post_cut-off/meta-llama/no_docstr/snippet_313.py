
import os
from typing import List


class ContentMixin:

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        content_dir = os.path.join(os.path.dirname(__file__), sub_folder)
        return [f for f in os.listdir(content_dir) if os.path.splitext(f)[1].lstrip('.') in extensions]

    def list_available_worlds(self) -> List[str]:
        return self._list_content_files('worlds', ['json'])

    def list_available_addons(self) -> List[str]:
        return self._list_content_files('addons', ['zip', 'py'])
