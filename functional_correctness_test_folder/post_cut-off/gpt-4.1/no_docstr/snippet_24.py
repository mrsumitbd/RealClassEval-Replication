
import re
from typing import List


class LocalPathExtractor:

    @staticmethod
    def is_local_path(path: str) -> bool:
        # Windows absolute: C:\ or D:/, etc.
        if re.match(r'^[a-zA-Z]:[\\/]', path):
            return True
        # Unix absolute: /
        if path.startswith('/'):
            return True
        # Relative: ./, ../, or just a filename or folder (not starting with http://, https://, ftp://, etc.)
        if path.startswith('./') or path.startswith('../'):
            return True
        # Exclude URLs and UNC paths
        if re.match(r'^(https?|ftp|file)://', path):
            return False
        if path.startswith('\\\\'):
            return False
        # Heuristic: contains at least one / or \ and not a URL
        if ('/' in path or '\\' in path) and not re.match(r'^\w+://', path):
            return True
        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        # Regex for Windows and Unix paths
        # Windows: C:\path\to\file or C:/path/to/file
        win_path = r'[a-zA-Z]:[\\/](?:[\w\-. ]+[\\/])*[\w\-. ]+'
        # Unix: /path/to/file
        unix_path = r'/[\w\-. /]+'
        # Relative: ./file, ../file, folder/file
        rel_path = r'(?:\.\.?/)+[\w\-. /]+'
        # Simple folder/file (not starting with protocol)
        simple_path = r'(?:[\w\-. ]+[\\/])+[\w\-. ]+'
        # Combine all
        pattern = f'({win_path})|({unix_path})|({rel_path})|({simple_path})'
        matches = re.findall(pattern, text)
        # Flatten and filter
        paths = []
        for match in matches:
            for m in match:
                if m and LocalPathExtractor.is_local_path(m):
                    paths.append(m)
        return paths
