
import os
from typing import List


class AppFileNotFoundError(Exception):
    pass


class FileOperationError(Exception):
    pass


class ContentMixin:

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        content_dir = self._content_dir
        if not content_dir or not os.path.isdir(content_dir):
            raise AppFileNotFoundError(
                f"The main content directory {content_dir} is not configured or does not exist.")

        target_dir = os.path.join(content_dir, sub_folder)
        if not os.path.isdir(target_dir):
            return []

        try:
            files = []
            for ext in extensions:
                files.extend([os.path.join(target_dir, f)
                             for f in os.listdir(target_dir) if f.endswith(ext)])
            return sorted(files)
        except OSError as e:
            raise FileOperationError(
                f"An error occurred while scanning the directory {target_dir}: {e}")

    def list_available_worlds(self) -> List[str]:
        return self._list_content_files("worlds", [".mcworld"])

    def list_available_addons(self) -> List[str]:
        return self._list_content_files("addons", [".mcpack", ".mcaddon"])
