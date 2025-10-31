from pathlib import Path
from demosys.exceptions import ImproperlyConfigured
from demosys.conf import settings

class BaseFileSystemFinder:
    """Base class for searching directory lists"""
    settings_attr = None

    def __init__(self):
        if not hasattr(settings, self.settings_attr):
            raise ImproperlyConfigured("Settings module don't define {}.This is required when using a FileSystemFinder.".format(self.settings_attr))
        self.paths = getattr(settings, self.settings_attr)

    def find(self, path: Path):
        """
        Find a file in the path. The file may exist in multiple
        paths. The last found file will be returned.

        :param path: The path to find
        :return: The absolute path to the file or None if not found
        """
        if getattr(self, 'settings_attr', None):
            self.paths = getattr(settings, self.settings_attr)
        path_found = None
        for entry in self.paths:
            abspath = entry / path
            if abspath.exists():
                path_found = abspath
        return path_found