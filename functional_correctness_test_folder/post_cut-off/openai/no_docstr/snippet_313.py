
import os
from typing import List


class ContentMixin:
    """
    Mixin providing helper methods to list content files such as worlds and addons.
    The content files are expected to be located under a ``content`` directory
    relative to the module's location.  The directory structure is assumed to be:

        content/
            worlds/
                <world files>
            addons/
                <addon files>

    The helper methods return the file names (without extensions) that match
    the requested extensions.
    """

    # Base directory where content is stored (relative to this file)
    _BASE_DIR = os.path.join(os.path.dirname(__file__), "content")

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        """
        List files in ``sub_folder`` under the base content directory that
        have one of the specified ``extensions``.

        Parameters
        ----------
        sub_folder : str
            Subdirectory under the base content directory (e.g. ``"worlds"``).
        extensions : List[str]
            List of file extensions to filter by (e.g. ``["json", "world"]``).
            Extensions should be provided without the leading dot.

        Returns
        -------
        List[str]
            Sorted list of file names (without extensions) that match the
            criteria.
        """
        folder_path = os.path.join(self._BASE_DIR, sub_folder)
        if not os.path.isdir(folder_path):
            return []

        # Normalise extensions to lower case for case‑insensitive matching
        ext_set = {ext.lower().lstrip(".") for ext in extensions}

        files = []
        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            if not os.path.isfile(full_path):
                continue
            name, ext = os.path.splitext(entry)
            if ext.lower().lstrip(".") in ext_set:
                files.append(name)

        return sorted(files)

    def list_available_worlds(self) -> List[str]:
        """
        Return a sorted list of available world names.

        World files are expected to be located in ``content/worlds`` and
        may have extensions such as ``.json`` or ``.world``.
        """
        return self._list_content_files("worlds", ["json", "world"])

    def list_available_addons(self) -> List[str]:
        """
        Return a sorted list of available addon names.

        Addon files are expected to be located in ``content/addons`` and
        may have extensions such as ``.zip`` or ``.addon``.
        """
        return self._list_content_files("addons", ["zip", "addon"])
