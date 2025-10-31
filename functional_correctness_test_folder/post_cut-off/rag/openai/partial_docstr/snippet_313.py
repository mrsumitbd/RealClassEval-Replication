
from pathlib import Path
from typing import List

# These exception classes are expected to be defined elsewhere in the project.
# They are imported here for type‑checking and to raise the correct errors.
try:
    from myproject.exceptions import AppFileNotFoundError, FileOperationError
except Exception:  # pragma: no cover
    # Fallback definitions for environments where the real exceptions are not available.
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
        Internal helper to list files with specified extensions from a sub‑folder
        within the global content directory.
        """
        # Resolve the global content directory if it hasn't been cached yet.
        if getattr(self, "_content_dir", None) is None:
            try:
                content_path = self.settings["paths.content"]
            except Exception as exc:  # pragma: no cover
                raise AppFileNotFoundError(
                    "Content directory not configured in settings['paths.content']"
                ) from exc

            if not content_path:
                raise AppFileNotFoundError(
                    "Content directory path is empty or None in settings['paths.content']"
                )

            self._content_dir = Path(content_path).expanduser().resolve()

        # Verify that the content directory exists and is a directory.
        if not self._content_dir.is_dir():
            raise AppFileNotFoundError(
                f"Content directory '{self._content_dir}' does not exist or is not a directory"
            )

        # Build the target sub‑folder path.
        target_dir = self._content_dir / sub_folder

        # If the sub‑folder does not exist, return an empty list.
        if not target_dir.is_dir():
            return []

        # Collect matching files.
        try:
            matched_files: List[Path] = []
            for ext in extensions:
                # Use glob to find files with the given extension.
                matched_files.extend(target_dir.glob(f"*{ext}"))
            # Convert to absolute string paths and sort.
            return sorted(str(p.resolve()) for p in matched_files if p.is_file())
        except OSError as exc:
            raise FileOperationError(
                f"Error scanning directory '{target_dir}': {exc}"
            ) from exc

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
