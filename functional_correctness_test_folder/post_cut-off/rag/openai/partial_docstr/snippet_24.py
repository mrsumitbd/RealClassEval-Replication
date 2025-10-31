
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''

    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        if not isinstance(path, str):
            return False
        # Windows drive letter
        if re.match(r'^[a-zA-Z]:[\\/]', path):
            return True
        # Unix absolute path
        if path.startswith('/'):
            return True
        # Relative path starting with ./ or ../
        if path.startswith('./') or path.startswith('../'):
            return True
        # Relative path without leading dot (e.g., "folder/file.txt")
        if re.match(r'^[^/\\]+[\\/][^/\\]+', path):
            return True
        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        if not isinstance(text, str):
            return []

        # Regex to capture potential local paths
        pattern = re.compile(
            r'''
            (?:
                # Windows drive letter
                [a-zA-Z]:[\\/]
                |
                # Unix absolute path
                /
                |
                # Relative paths starting with ./ or ../
                \.{1,2}[\\/]
                |
                # Other relative paths (no leading slash or dot)
                [^ \t\n\r\f\v/\\]+[\\/]
            )
            [^ \t\n\r\f\v]+
            ''',
            re.VERBOSE
        )

        matches = pattern.findall(text)
        paths = []
        for m in matches:
            # Strip trailing punctuation
            cleaned = m.rstrip('.,;:!?)]}\'"')
            # Exclude URLs
            if re.match(r'^(http|https)://', cleaned):
                continue
            if LocalPathExtractor.is_local_path(cleaned):
                paths.append(cleaned)
        return paths
