from typing import List
import os


class ContentMixin:
    '''
    Mixin class for BedrockServerManager that handles global content management.
    '''

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        '''
        Internal helper to list files with specified extensions from a sub-folder
        within the global content directory.
        '''
        # Check if _content_dir is set and is a directory
        content_dir = getattr(self, '_content_dir', None)
        if not content_dir or not os.path.isdir(content_dir):
            from .exceptions import AppFileNotFoundError
            raise AppFileNotFoundError(
                f"Content directory '{content_dir}' not found or not configured.")

        target_dir = os.path.join(content_dir, sub_folder)
        if not os.path.isdir(target_dir):
            # If the subfolder doesn't exist, return empty list
            return []

        try:
            files = []
            for entry in os.listdir(target_dir):
                full_path = os.path.join(target_dir, entry)
                if os.path.isfile(full_path):
                    _, ext = os.path.splitext(entry)
                    if ext.lower() in [e.lower() for e in extensions]:
                        files.append(os.path.abspath(full_path))
            return sorted(files)
        except OSError as e:
            from .exceptions import FileOperationError
            raise FileOperationError(
                f"Error scanning directory '{target_dir}': {e}")

    def list_available_worlds(self) -> List[str]:
        '''Lists available ``.mcworld`` template files from the global content directory.'''
        return self._list_content_files("worlds", [".mcworld"])

    def list_available_addons(self) -> List[str]:
        '''Lists available addon files (``.mcpack``, ``.mcaddon``) from the global content directory.'''
        return self._list_content_files("addons", [".mcpack", ".mcaddon"])
