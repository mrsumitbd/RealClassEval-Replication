
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
        if not hasattr(self, '_content_dir') or not self._content_dir:
            raise AppFileNotFoundError(
                "The main content directory is not configured.")

        target_dir = os.path.join(self._content_dir, sub_folder)

        if not os.path.isdir(target_dir):
            raise AppFileNotFoundError(
                f"The target directory {target_dir} does not exist.")

        try:
            files = [os.path.join(target_dir, f) for f in os.listdir(
                target_dir) if any(f.endswith(ext) for ext in extensions)]
            return sorted(files)
        except OSError as e:
            raise FileOperationError(
                f"An error occurred while scanning the directory: {e}")

    def list_available_worlds(self) -> List[str]:
        '''Lists available ``.mcworld`` template files from the global content directory.'''
        return self._list_content_files("worlds", [".mcworld"])

    def list_available_addons(self) -> List[str]:
        '''Lists available addon files (``.mcpack``, ``.mcaddon``) from the global content directory.'''
        return self._list_content_files("addons", [".mcpack", ".mcaddon"])
