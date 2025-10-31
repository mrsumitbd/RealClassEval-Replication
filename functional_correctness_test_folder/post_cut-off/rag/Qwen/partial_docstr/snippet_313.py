
import os
from pathlib import Path
from typing import List


class AppFileNotFoundError(Exception):
    pass


class FileOperationError(Exception):
    pass


class ContentMixin:
    '''
    Mixin class for BedrockServerManager that handles global content management.
    '''

    def __init__(self, settings):
        self._content_dir = Path(settings['paths.content'])

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        '''
        Internal helper to list files with specified extensions from a sub-folder
        within the global content directory.
        '''
        target_dir = self._content_dir / sub_folder
        if not target_dir.exists() or not target_dir.is_dir():
            raise AppFileNotFoundError(
                f"The directory {target_dir} does not exist or is not a directory.")

        try:
            files = [str(f.resolve()) for f in target_dir.iterdir()
                     if f.is_file() and f.suffix in extensions]
            return sorted(files)
        except OSError as e:
            raise FileOperationError(
                f"An error occurred while scanning the directory {target_dir}: {e}")

    def list_available_worlds(self) -> List[str]:
        '''Lists available ``.mcworld`` template files from the global content directory.'''
        return self._list_content_files('worlds', ['.mcworld'])

    def list_available_addons(self) -> List[str]:
        '''Lists available addon files (``.mcpack``, ``.mcaddon``) from the global content directory.'''
        return self._list_content_files('addons', ['.mcpack', '.mcaddon'])
