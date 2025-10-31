
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

    def __init__(self, settings, content_dir_attr='_content_dir'):
        self.settings = settings
        self._content_dir = None
        self._content_dir_attr = content_dir_attr

    @property
    def content_dir(self):
        if not hasattr(self, self._content_dir_attr):
            raise AppFileNotFoundError(
                "Main content directory is not configured")
        content_dir = getattr(self, self._content_dir_attr)
        if content_dir is None:
            content_dir = self.settings['paths.content']
            setattr(self, self._content_dir_attr, content_dir)
        if not os.path.isdir(content_dir):
            raise AppFileNotFoundError("Main content directory does not exist")
        return content_dir

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        '''
        Internal helper to list files with specified extensions from a sub-folder
        within the global content directory.
        '''
        content_dir = self.content_dir
        target_dir = os.path.join(content_dir, sub_folder)
        try:
            files = os.listdir(target_dir) if os.path.exists(
                target_dir) else []
        except OSError as e:
            raise FileOperationError(f"Error scanning directory: {e}")
        matching_files = [os.path.join(target_dir, f) for f in files if os.path.splitext(f)[
            1].lower() in extensions]
        return sorted(matching_files)

    def list_available_worlds(self) -> List[str]:
        '''Lists available ``.mcworld`` template files from the global content directory.
        '''
        return self._list_content_files('worlds', ['.mcworld'])

    def list_available_addons(self) -> List[str]:
        '''Lists available addon files (``.mcpack``, ``.mcaddon``) from the global content directory.
        '''
        return self._list_content_files('addons', ['.mcpack', '.mcaddon'])
