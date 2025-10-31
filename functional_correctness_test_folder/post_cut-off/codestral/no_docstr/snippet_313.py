
import os
from typing import List


class ContentMixin:

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        content_files = []
        for root, dirs, files in os.walk(sub_folder):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    content_files.append(os.path.join(root, file))
        return content_files

    def list_available_worlds(self) -> List[str]:
        return self._list_content_files('worlds', ['.world'])

    def list_available_addons(self) -> List[str]:
        return self._list_content_files('addons', ['.addon'])
