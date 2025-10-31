
from typing import List
import os
from pathlib import Path

# Assume these exceptions are defined elsewhere in the project


class AppFileNotFoundError(Exception):
    pass


class FileOperationError(Exception):
    pass


class ContentMixin:
    """
    Mixin providing helper methods for listing content files
    (worlds and addons) from the application's global content
    directory.
    """

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        """
        Internal helper to list files with specified extensions from a sub-folder
        within the global content directory.
        """
        # Ensure the main content directory is configured
        content_dir = getattr(self, "_content_dir", None)
        if not content_dir:
            raise AppFileNotFoundError("Content directory is not configured.")

        # Resolve the target directory
        target_dir = Path(content_dir) / sub_folder

        # If the target directory does not exist or is not a directory, return empty list
        if not target_dir.is_dir():
            return []

        try:
            # Gather all files in the directory that match the extensions
            files = [
                str(file.resolve())
                for file in target_dir.iterdir()
                if file.is_file() and file.suffix in extensions
            ]
        except OSError as exc:
            raise FileOperationError(
                f"Error scanning directory '{target_dir}': {exc}") from exc

        # Return a sorted list of absolute paths
        return sorted(files)

    def list_available_worlds(self) -> List[str]:
        """
        List available world files (.mcworld) from the global content directory.
        """
        return self._list_content_files("worlds", [".mcworld"])

    def list_available_addons(self) -> List[str]:
        """
        List available addon files (.mcpack, .mcaddon) from the global content directory.
        """
        return self._list_content_files("addons", [".mcpack", ".mcaddon"])
