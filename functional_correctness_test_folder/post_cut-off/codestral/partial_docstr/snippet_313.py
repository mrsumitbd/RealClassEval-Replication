
import os
from typing import List
from pathlib import Path


class ContentMixin:
    def __init__(self):
        self._content_dir = Path(settings['paths.content'])

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        content_subdir = self._content_dir / sub_folder
        if not self._content_dir.exists():
            raise AppFileNotFoundError(
                f"Content directory not found: {self._content_dir}")
        if not content_subdir.exists():
            return []

        try:
            files = []
            for ext in extensions:
                files.extend(content_subdir.glob(f"*{ext}"))
            return sorted([str(file) for file in files])
        except OSError as e:
            raise FileOperationError(
                f"Error scanning directory {content_subdir}: {e}")

    def list_available_worlds(self) -> List[str]:
        return self._list_content_files("worlds", [".mcworld"])

    def list_available_addons(self) -> List[str]:
        return self._list_content_files("addons", [".mcpack", ".mcaddon"])
