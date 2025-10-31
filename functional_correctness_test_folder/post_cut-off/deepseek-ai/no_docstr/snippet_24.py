
import re
from typing import List


class LocalPathExtractor:

    @staticmethod
    def is_local_path(path: str) -> bool:
        # Check for Unix-like paths (absolute or relative)
        if path.startswith('/') or path.startswith('./') or path.startswith('../'):
            return True
        # Check for Windows-like paths (absolute or relative)
        if re.match(r'^[a-zA-Z]:\\', path) or re.match(r'^\\', path) or re.match(r'^\.\\', path):
            return True
        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        # Pattern for Unix-like paths
        unix_pattern = r'(?:/[^/ \n]+)+|(?:\.{1,2}/[^/ \n]+)+'
        # Pattern for Windows-like paths
        windows_pattern = r'(?:[a-zA-Z]:\\(?:[^\\ \n]+\\)*[^\\ \n]+)|(?:\\(?:[^\\ \n]+\\)*[^\\ \n]+)|(?:\.\\(?:[^\\ \n]+\\)*[^\\ \n]+)'
        combined_pattern = f'({unix_pattern}|{windows_pattern})'
        matches = re.findall(combined_pattern, text)
        # Flatten the matches and filter valid paths
        paths = [match[0] or match[1] for match in matches]
        return [path for path in paths if LocalPathExtractor.is_local_path(path)]
