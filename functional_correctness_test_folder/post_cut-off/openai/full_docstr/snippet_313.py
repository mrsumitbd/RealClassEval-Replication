
from typing import List
import os

# These exceptions are expected to be defined elsewhere in the project.
# Import them here; if they are not available, the import will fail
# and the user will need to provide appropriate definitions.
try:
    from .exceptions import AppFileNotFoundError, FileOperationError
except Exception:  # pragma: no cover
    # Fallback minimal definitions for standalone use
    class AppFileNotFoundError(FileNotFoundError):
        """Raised when a required application file or directory is missing."""
        pass

    class FileOperationError(OSError):
        """Raised when an OS-level file operation fails."""
        pass


class ContentMixin:
    """
    Mixin class for BedrockServerManager that handles global content management.
    """

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        """
        Internal helper to list files with specified extensions from a sub-folder
        within the global content directory.
        This method constructs a path to ``<content_dir>/<sub_folder>``, then
        scans this directory for files matching any of the provided ``extensions``.
        The global content directory is defined by ``settings['paths.content']``
        and cached in :attr:`._content_dir`.
        Args:
            sub_folder (str): The name of the sub-folder within the global content
                directory to scan (e.g., "worlds", "addons").
            extensions (List[str]): A list of file extensions to search for.
                Extensions should include the leading dot (e.g., ``[".mcworld"]``,
                ``[".mcpack", ".mcaddon"]``).
        Returns:
            List[str]: A sorted list of absolute paths to the files found.
            Returns an empty list if the target directory does not exist or no
            matching files are found.
        Raises:
            AppFileNotFoundError: If the main content directory (:attr:`._content_dir`)
                is not configured or does not exist as a directory.
            FileOperationError: If an OS-level error occurs while scanning the
                directory (e.g., permission issues).
        """
        # Resolve the global content directory if not already cached
        if not hasattr(self, "_content_dir") or not self._content_dir:
            try:
                self._content_dir = self.settings["paths.content"]
            except Exception as exc:  # pragma: no cover
                raise AppFileNotFoundError(
                    "Global content directory not configured in settings."
                ) from exc

        # Validate that the content directory exists and is a directory
        if not os.path.isdir(self._content_dir):
            raise AppFileNotFoundError(
                f"Global content directory '{self._content_dir}' does not exist or is not a directory."
            )

        # Build the full path to the sub-folder
        target_dir = os.path.join(self._content_dir, sub_folder)

        # If the sub-folder does not exist, return an empty list
        if not os.path.isdir(target_dir):
            return []

        try:
            # List all entries in the target directory
            entries = os.listdir(target_dir)
        except OSError as exc:
            raise FileOperationError(
                f"Error accessing directory '{target_dir}': {exc}"
            ) from exc

        # Filter entries by file extension and ensure they are files
        matched_files = []
        for entry in entries:
            full_path = os.path.join(target_dir, entry)
            if os.path.isfile(full_path) and os.path.splitext(entry)[1] in extensions:
                matched_files.append(os.path.abspath(full_path))

        # Return a sorted list of absolute paths
        return sorted(matched_files)

    def list_available_worlds(self) -> List[str]:
        """
        Lists available ``.mcworld`` template files from the global content directory.
        This method scans the ``worlds`` sub-folder within the application's
        global content directory (see :attr:`._content_dir` and
        ``settings['paths.content']``) for files with the ``.mcworld`` extension.
        It relies on :meth:`._list_content_files` for the actual scanning.
        These ``.mcworld`` files typically represent world templates that can be
        imported to create new server worlds or overwrite existing ones.
        Returns:
            List[str]: A sorted list of absolute paths to all found ``.mcworld`` files.
            Returns an empty list if the directory doesn't exist or no ``.mcworld``
            files are present.
        Raises:
            AppFileNotFoundError: If the main content directory is not configured
                or found (from :meth:`._list_content_files`).
            FileOperationError: If an OS error occurs during directory scanning
                (from :meth:`._list_content_files`).
        """
        return self._list_content_files("worlds", [".mcworld"])

    def list_available_addons(self) -> List[str]:
        """
        Lists available addon files (``.mcpack``, ``.mcaddon``) from the global content directory.
        This method scans the ``addons`` sub-folder within the application's
        global content directory (see :attr:`._content_dir` and
        ``settings['paths.content']``) for files with ``.mcpack`` or
        ``.mcaddon`` extensions. It uses :meth:`._list_content_files` for scanning.
        These files represent behavior packs, resource packs, or bundled addons
        that can be installed onto server instances.
        Returns:
            List[str]: A sorted list of absolute paths to all found ``.mcpack``
            and ``.mcaddon`` files. Returns an empty list if the directory
            doesn't exist or no such files are present.
        Raises:
            AppFileNotFoundError: If the main content directory is not configured
                or found (from :meth:`._list_content_files`).
            FileOperationError: If an OS error occurs during directory scanning
                (from :meth:`._list_content_files`).
        """
        return self._list_content_files("addons", [".mcpack", ".mcaddon"])
