
import os
from typing import List


class ContentMixin:

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        base_dir = getattr(self, 'content_dir', None)
        if base_dir is None:
            raise AttributeError(
                "Class using ContentMixin must have a 'content_dir' attribute.")
        folder_path = os.path.join(base_dir, sub_folder)
        if not os.path.isdir(folder_path):
            return []
        files = []
        for fname in os.listdir(folder_path):
            if any(fname.lower().endswith(ext.lower()) for ext in extensions):
                files.append(fname)
        return sorted(files)

    def list_available_worlds(self) -> List[str]:
        return self._list_content_files('worlds', ['.world', '.wld'])

    def list_available_addons(self) -> List[str]:
        return self._list_content_files('addons', ['.addon', '.zip'])
