
import re
from typing import List


class LocalPathExtractor:

    @staticmethod
    def is_local_path(path: str) -> bool:
        """Check if the given path is a local path."""
        # A local path should start with a drive letter (Windows) or be relative/absolute path (Unix-based)
        # or start with './' or '../'
        pattern = re.compile(r'^([a-zA-Z]:|/|\\|\.{1,2}/)')
        return bool(pattern.match(path))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        """Extract local paths from the given text."""
        # Regular expression pattern to match local paths
        pattern = re.compile(
            r'([a-zA-Z]:[\/\\][\w\.\/\\-]+|[\/\\][\w\.\/\\-]+|\.{1,2}/[\w\.\/\-]+)')
        return pattern.findall(text)
