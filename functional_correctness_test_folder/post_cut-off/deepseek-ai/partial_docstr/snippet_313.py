
import os
from typing import List


class ContentMixin:

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        content_dir = getattr(self, '_content_dir', None)
        if not content_dir:
            raise AppFileNotFoundError("Content directory is not configured.")

        target_dir = os.path.join(content_dir, sub_folder)
        if not os.path.isdir(target_dir):
            return []

        try:
            files = []
            for entry in os.listdir(target_dir):
                full_path = os.path.join(target_dir, entry)
                if os.path.isfile(full_path) and any(entry.lower().endswith(ext) for ext in extensions):
                    files.append(full_path)
            return sorted(files)
        except OSError as e:
            raise FileOperationError(f"Error scanning directory: {e}")

    def list_available_worlds(self) -> List[str]:
        return self._list_content_files("worlds", [".mcworld"])

    def list_available_addons(self) -> List[str]:
        return self._list_content_files("addons", [".mcpack", ".mcaddon"])


class AppFileNotFoundError(Exception):
    pass


class FileOperationError(Exception):
    pass
