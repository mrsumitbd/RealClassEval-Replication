from typing import List
import os


class ContentMixin:
    def _get_content_root(self) -> str:
        for attr in ("content_dir", "content_root", "base_content_dir", "base_dir", "root_dir", "data_dir", "path"):
            if hasattr(self, attr) and getattr(self, attr):
                return os.fspath(getattr(self, attr))
        return os.getcwd()

    def _list_content_files(self, sub_folder: str, extensions: List[str]) -> List[str]:
        base_root = self._get_content_root()
        target_dir = os.path.join(base_root, sub_folder)
        if not os.path.isdir(target_dir):
            return []

        exts = set()
        if extensions:
            for e in extensions:
                if not e:
                    continue
                exts.add(e.lower() if e.startswith(".") else f".{e.lower()}")

        names = set()
        for root, _, files in os.walk(target_dir):
            for f in files:
                stem, ext = os.path.splitext(f)
                if not exts or ext.lower() in exts:
                    names.add(stem)
        return sorted(names)

    def list_available_worlds(self) -> List[str]:
        base_root = self._get_content_root()
        worlds_dir = os.path.join(base_root, "worlds")

        names = set()

        # Include directory-based worlds (immediate children only)
        if os.path.isdir(worlds_dir):
            try:
                for entry in os.scandir(worlds_dir):
                    if entry.is_dir():
                        names.add(entry.name)
            except FileNotFoundError:
                pass

        # Include file-based worlds by common extensions
        file_worlds = self._list_content_files(
            "worlds", [".mcworld", ".zip", ".world"])
        names.update(file_worlds)

        return sorted(names)

    def list_available_addons(self) -> List[str]:
        base_root = self._get_content_root()
        addons_dir = os.path.join(base_root, "addons")

        names = set()

        # Include directory-based addons (immediate children only)
        if os.path.isdir(addons_dir):
            try:
                for entry in os.scandir(addons_dir):
                    if entry.is_dir():
                        names.add(entry.name)
            except FileNotFoundError:
                pass

        # Include file-based addons by common extensions
        file_addons = self._list_content_files(
            "addons", [".mcaddon", ".zip", ".addon"])
        names.update(file_addons)

        return sorted(names)
