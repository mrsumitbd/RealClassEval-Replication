
import os
from typing import List


class AppFileNotFoundError(Exception):
    pass


class FileOperationError(Exception):
    pass


class ContentMixin:
    _content_dir = None
    # Assuming this is defined somewhere else in the class or application
    settings = {'paths': {'content': None}}

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        if not self._content_dir or not os.path.isdir(self._content_dir):
            raise AppFileNotFoundError(
                "Main content directory is not configured or does not exist.")

        target_dir = os.path.join(self._content_dir, sub_folder)

        try:
            files = os.listdir(target_dir)
        except FileNotFoundError:
            return []
        except OSError as e:
            raise FileOperationError(f"Error scanning directory: {e}")

        matching_files = [os.path.abspath(os.path.join(target_dir, file))
                          for file in files
                          if os.path.isfile(os.path.join(target_dir, file))
                          and os.path.splitext(file)[1].lower() in [ext.lower() for ext in extensions]]

        return sorted(matching_files)

    def list_available_worlds(self) -> List[str]:
        return self._list_content_files('worlds', ['.mcworld'])

    def list_available_addons(self) -> List[str]:
        return self._list_content_files('addons', ['.mcpack', '.mcaddon'])


# Example usage
if __name__ == "__main__":
    content_mixin = ContentMixin()
    content_mixin._content_dir = '/path/to/content/directory'
    content_mixin.settings['paths']['content'] = '/path/to/content/directory'

    try:
        worlds = content_mixin.list_available_worlds()
        addons = content_mixin.list_available_addons()
        print("Available Worlds:", worlds)
        print("Available Addons:", addons)
    except (AppFileNotFoundError, FileOperationError) as e:
        print("Error:", e)
