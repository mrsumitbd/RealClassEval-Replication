
from typing import List
import os


class ContentMixin:

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        content_dir = os.path.join(os.path.dirname(__file__), sub_folder)
        if not os.path.exists(content_dir):
            return []

        files = []
        for file in os.listdir(content_dir):
            if any(file.endswith(ext) for ext in extensions):
                files.append(file)
        return files

    def list_available_worlds(self) -> List[str]:
        return self._list_content_files("worlds", [".world", ".sdf"])

    def list_available_addons(self) -> List[str]:
        return self._list_content_files("addons", [".addon", ".plugin"])
