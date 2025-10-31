
from pathlib import Path
from typing import List

# The following imports assume that the exception classes are defined
# somewhere in the project. Adjust the import path as necessary.
try:
    from .exceptions import AppFileNotFoundError, FileOperationError
except Exception:  # pragma: no cover
    # Fallback definitions for environments where the real exceptions
    # are not available. Replace these with the actual imports in
    # production code.
    class AppFileNotFoundError(FileNotFoundError):
        pass

    class FileOperationError(OSError):
        pass


class ContentMixin:
    """
    Mixin class for BedrockServerManager that handles global content management.
    """

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        """
        Internal helper to list files with specified extensions from a sub-folder
        within the global content directory.
        """
        # Resolve the main content directory
        if not hasattr(self, "_content_dir") or self._content_dir is None:
            raise AppFileNotFoundError("Content directory not configured")

        content_dir = Path(self._content_dir)
        if not content_dir.is_dir():
            raise AppFileNotFoundError(
                f"Content directory '{content_dir}' does not exist or is not a directory")

        # Build the target sub-folder path
        target_dir = content_dir / sub_folder
        if not target_dir.is_dir():
            # If the sub-folder does not exist, return an empty list
            return []

        try:
            # Collect files that match any of the provided extensions
            matched_files = []
            for ext in extensions:
                # Use glob to find files with the given suffix
                matched_files.extend(target_dir.glob(f"*{ext}"))

            # Convert to absolute string paths and sort
            result = sorted(str(p.resolve())
                            for p in matched_files if p.is_file())
            return result
        except OSError as exc:
            raise FileOperationError(
                f"Error scanning directory '{target_dir}': {exc}") from exc

    def list_available_worlds(self) -> List[str]:
        """
        Lists available ``.mcworld`` template files from the global content directory.
        """
        return self._list_content_files("worlds", [".mcworld"])

    def list_available_addons(self) -> List[str]:
        """
        Lists available addon files (``.mcpack``, ``.mcaddon``) from the global content directory.
        """
        return self._list_content_files("addons", [".mcpack", ".mcaddon"])
