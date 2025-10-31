
from pathlib import Path
from typing import List


class ContentMixin:
    '''
    Mixin class for BedrockServerManager that handles global content management.
    '''

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        '''
        Internal helper to list files with specified extensions from a sub-folder
        within the global content directory.
        '''
        # Resolve the global content directory
        if not hasattr(self, "_content_dir") or self._content_dir is None:
            try:
                content_path = self.settings["paths.content"]
            except Exception as exc:
                raise AppFileNotFoundError(
                    "Global content directory not configured in settings"
                ) from exc

            if not content_path:
                raise AppFileNotFoundError(
                    "Global content directory not configured in settings"
                )

            self._content_dir = Path(content_path).resolve()

        content_dir = Path(self._content_dir)

        if not content_dir.is_dir():
            raise AppFileNotFoundError(
                f"Global content directory '{content_dir}' does not exist or is not a directory"
            )

        target_dir = content_dir / sub_folder

        if not target_dir.is_dir():
            # Directory does not exist – return empty list
            return []

        try:
            files = []
            for ext in extensions:
                # Use glob to find files with the given extension
                for file_path in target_dir.rglob(f"*{ext}"):
                    if file_path.is_file():
                        files.append(str(file_path.resolve()))
            return sorted(files)
        except OSError as exc:
            raise FileOperationError(
                f"Error scanning directory '{target_dir}': {exc}"
            ) from exc

    def list_available_worlds(self) -> List[str]:
        '''Lists available ``.mcworld`` template files from the global content directory.'''
        return self._list_content_files("worlds", [".mcworld"])

    def list_available_addons(self) -> List[str]:
        '''Lists available addon files (``.mcpack``, ``.mcaddon``) from the global content directory.'''
        return self._list_content_files("addons", [".mcpack", ".mcaddon"])
