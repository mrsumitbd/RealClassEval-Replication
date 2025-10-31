from typing import List
from pathlib import Path
import os


class ContentMixin:
    '''
    Mixin class for BedrockServerManager that handles global content management.
        '''

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        '''
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
        '''
        # Resolve and validate the global content directory, cache if needed
        content_dir = getattr(self, '_content_dir', None)
        if not content_dir:
            settings = getattr(self, 'settings', {}) or {}
            content_path = None
            if isinstance(settings, dict):
                # Support both dotted key and nested dict
                content_path = settings.get('paths.content')
                if content_path is None:
                    paths_section = settings.get('paths')
                    if isinstance(paths_section, dict):
                        content_path = paths_section.get('content')

            if not content_path:
                raise AppFileNotFoundError(
                    "Global content directory is not configured (settings['paths.content']).")

            content_dir = Path(content_path)
        else:
            content_dir = Path(content_dir)

        if not content_dir.exists() or not content_dir.is_dir():
            raise AppFileNotFoundError(
                f"Global content directory does not exist or is not a directory: {content_dir}")

        # Cache the resolved path
        self._content_dir = content_dir

        target_dir = content_dir / sub_folder
        if not target_dir.exists() or not target_dir.is_dir():
            return []

        if not extensions:
            return []

        exts = {ext.lower() for ext in extensions}
        results: List[str] = []

        try:
            with os.scandir(target_dir) as it:
                for entry in it:
                    try:
                        if not entry.is_file():
                            continue
                        suffix = Path(entry.name).suffix.lower()
                        if suffix in exts:
                            results.append(str(Path(entry.path).resolve()))
                    except OSError:
                        # Skip entries that cannot be accessed/stat'ed
                        continue
        except OSError as e:
            raise FileOperationError(
                f"Error scanning directory '{target_dir}': {e}") from e

        results.sort(key=lambda p: p.lower())
        return results

    def list_available_worlds(self) -> List[str]:
        '''Lists available ``.mcworld`` template files from the global content directory.
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
        '''
        return self._list_content_files('worlds', ['.mcworld'])

    def list_available_addons(self) -> List[str]:
        '''Lists available addon files (``.mcpack``, ``.mcaddon``) from the global content directory.
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
        '''
        return self._list_content_files('addons', ['.mcpack', '.mcaddon'])
