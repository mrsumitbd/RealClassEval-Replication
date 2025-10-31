import os
from towncrier._settings.load import Config

class FragmentsPath:
    """
    A helper to get the full path to a fragments directory.

    This is a callable that optionally takes a section directory and returns the full
    path to the fragments directory for that section (or the default if no section is
    provided).
    """

    def __init__(self, base_directory: str, config: Config):
        self.base_directory = base_directory
        self.config = config
        if config.directory is not None:
            self.base_directory = os.path.abspath(os.path.join(base_directory, config.directory))
            self.append_directory = ''
        else:
            self.base_directory = os.path.abspath(os.path.join(base_directory, config.package_dir, config.package))
            self.append_directory = 'newsfragments'

    def __call__(self, section_directory: str='') -> str:
        return os.path.join(self.base_directory, section_directory, self.append_directory)