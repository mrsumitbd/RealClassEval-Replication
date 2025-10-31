
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        # Windows absolute: C:\ or D:/, relative: .\ or ..\
        # Unix absolute: /, relative: ./ or ../
        win_abs = re.compile(r'^[a-zA-Z]:[\\/](?:[^:*?"<>|\r\n]+[\\/]?)*$')
        win_rel = re.compile(r'^(\.{1,2}[\\/])(?:[^:*?"<>|\r\n]+[\\/]?)*$')
        unix_abs = re.compile(r'^/(?:[^:*?"<>|\r\n]+/?)*$')
        unix_rel = re.compile(r'^(\.{1,2}/)(?:[^:*?"<>|\r\n]+/?)*$')
        return bool(win_abs.match(path) or win_rel.match(path) or unix_abs.match(path) or unix_rel.match(path))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        # Patterns for Windows and Unix paths
        win_pattern = r'[a-zA-Z]:[\\/](?:[^:*?"<>|\s\r\n]+[\\/]?)*'
        win_rel_pattern = r'\.{1,2}[\\/](?:[^:*?"<>|\s\r\n]+[\\/]?)*'
        unix_pattern = r'/(?:[^:*?"<>|\s\r\n]+/?)*'
        unix_rel_pattern = r'\.{1,2}/(?:[^:*?"<>|\s\r\n]+/?)*'
        pattern = f'({win_pattern})|({win_rel_pattern})|({unix_pattern})|({unix_rel_pattern})'
        matches = re.findall(pattern, text)
        # Each match is a tuple, only one group is non-empty
        paths = [m[0] or m[1] or m[2] or m[3] for m in matches]
        # Filter out empty strings and ensure they are valid local paths
        return [p for p in paths if p and LocalPathExtractor.is_local_path(p)]
