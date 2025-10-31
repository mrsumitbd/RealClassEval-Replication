
import os
from typing import List


class AppFileNotFoundError(Exception):
    pass


class FileOperationError(Exception):
    pass


class ContentMixin:
    '''
    Mixin class for BedrockServerManager that handles global content management.
    '''

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        '''
        Internal helper to list files with specified extensions from a sub-folder
        within the global content directory.
        '''
        # Get the content directory from settings or attribute
        content_dir = getattr(self, '_content_dir', None)
        if content_dir is None:
            # Try to get from settings if available
            settings = getattr(self, 'settings', None)
            if settings and 'paths.content' in settings:
                content_dir = settings['paths.content']
                self._content_dir = content_dir
        if not content_dir or not isinstance(content_dir, str):
            raise AppFileNotFoundError(
                "Global content directory is not configured.")
        if not os.path.isdir(content_dir):
            raise AppFileNotFoundError(
                f"Global content directory '{content_dir}' does not exist.")

        target_dir = os.path.join(content_dir, sub_folder)
        if not os.path.isdir(target_dir):
            return []

        try:
            files = []
            for entry in os.scandir(target_dir):
                if entry.is_file():
                    _, ext = os.path.splitext(entry.name)
                    if ext.lower() in [e.lower() for e in extensions]:
                        files.append(os.path.abspath(entry.path))
            files.sort()
            return files
        except OSError as e:
            raise FileOperationError(
                f"Error scanning directory '{target_dir}': {e}")

    def list_available_worlds(self) -> List[str]:
        '''Lists available ``.mcworld`` template files from the global content directory.'''
        return self._list_content_files("worlds", [".mcworld"])

    def list_available_addons(self) -> List[str]:
        '''Lists available addon files (``.mcpack``, ``.mcaddon``) from the global content directory.'''
        return self._list_content_files("addons", [".mcpack", ".mcaddon"])
