
import os
from typing import List

# Dummy exception classes for completeness


class AppFileNotFoundError(Exception):
    pass


class FileOperationError(Exception):
    pass


# Dummy global settings for demonstration
settings = {
    # Example path; in real use, this would be set elsewhere
    'paths.content': '/tmp/content'
}


class ContentMixin:
    _content_dir = None

    def _get_content_dir(self):
        if self._content_dir is not None:
            return self._content_dir
        content_dir = settings.get('paths.content')
        if not content_dir or not isinstance(content_dir, str):
            raise AppFileNotFoundError("Content directory is not configured.")
        if not os.path.isdir(content_dir):
            raise AppFileNotFoundError(
                f"Content directory '{content_dir}' does not exist.")
        self._content_dir = content_dir
        return self._content_dir

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        try:
            content_dir = self._get_content_dir()
            target_dir = os.path.join(content_dir, sub_folder)
            if not os.path.isdir(target_dir):
                return []
            files = []
            for entry in os.scandir(target_dir):
                if entry.is_file():
                    _, ext = os.path.splitext(entry.name)
                    if ext.lower() in [e.lower() for e in extensions]:
                        files.append(os.path.abspath(entry.path))
            return sorted(files)
        except AppFileNotFoundError:
            raise
        except OSError as e:
            raise FileOperationError(
                f"Error scanning directory '{sub_folder}': {e}")

    def list_available_worlds(self) -> List[str]:
        # Worlds are typically .mcworld files in the 'worlds' subfolder
        return self._list_content_files('worlds', ['.mcworld'])

    def list_available_addons(self) -> List[str]:
        # Addons are .mcpack and .mcaddon files in the 'addons' subfolder
        return self._list_content_files('addons', ['.mcpack', '.mcaddon'])
