
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        # Check for Unix-like paths (absolute or relative)
        if path.startswith('/') or path.startswith('./') or path.startswith('../'):
            return True
        # Check for Windows-like paths (drive letters or UNC paths)
        if re.match(r'^[a-zA-Z]:\\', path) or path.startswith('\\\\'):
            return True
        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        # Pattern for Unix-like paths
        unix_pattern = r'(?:^|\s)(/(?:[^/\s]+/)*[^/\s]+|\.{1,2}/[^\s]*)'
        # Pattern for Windows-like paths
        windows_pattern = r'(?:^|\s)([a-zA-Z]:\\(?:[^\\\s]+\\)*[^\\\s]+|\\\\[^\\\s]+\\[^\s]*)'
        # Combine patterns
        combined_pattern = f'{unix_pattern}|{windows_pattern}'
        matches = re.findall(combined_pattern, text)
        # Flatten the matches and filter out empty strings
        paths = [match[0] or match[1]
                 for match in matches if match[0] or match[1]]
        return paths
