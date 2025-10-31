from typing import List
import os


class ContentMixin:

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
        content_dir = getattr(self, "_content_dir", None)

        if not content_dir:
            settings = getattr(self, "settings", {}) or {}
            paths_cfg = settings.get("paths", {}) if isinstance(
                settings, dict) else {}
            content_dir = paths_cfg.get("content")
            if content_dir:
                content_dir = os.path.abspath(
                    os.path.expanduser(str(content_dir)))
                setattr(self, "_content_dir", content_dir)

        if not content_dir or not os.path.isdir(content_dir):
            raise AppFileNotFoundError(
                "Content directory not configured or does not exist")

        target_dir = os.path.join(content_dir, sub_folder)
        if not os.path.isdir(target_dir):
            return []

        exts = {e.lower() for e in (extensions or [])
                if isinstance(e, str) and e}
        if not exts:
            return []

        try:
            results: List[str] = []
            with os.scandir(target_dir) as it:
                for entry in it:
                    if not entry.is_file():
                        continue
                    _, ext = os.path.splitext(entry.name)
                    if ext.lower() in exts:
                        results.append(os.path.abspath(entry.path))
            return sorted(results)
        except OSError as e:
            raise FileOperationError(
                f"Failed scanning directory '{target_dir}': {e}") from e

    def list_available_worlds(self) -> List[str]:
        return self._list_content_files("worlds", [".mcworld"])

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
        return self._list_content_files("addons", [".mcpack", ".mcaddon"])
