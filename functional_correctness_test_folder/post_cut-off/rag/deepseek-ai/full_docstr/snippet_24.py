
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        # Check for common local path patterns (Windows and Unix-like)
        return (path.startswith('/') or
                path.startswith('./') or
                path.startswith('../') or
                (len(path) > 1 and path[1] == ':' and path[2] == '\\') or
                path.startswith('~') or
                path.startswith('\\'))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        # Regex pattern to match common local paths (Windows and Unix-like)
        pattern = r'(?:[a-zA-Z]:[\\/]|~|\.{1,2}[\\/]|/|\\|\b\w:)[\w\.\-\\/]*'
        matches = re.findall(pattern, text)
        # Filter out non-path matches and return only valid local paths
        return [match for match in matches if LocalPathExtractor.is_local_path(match)]
