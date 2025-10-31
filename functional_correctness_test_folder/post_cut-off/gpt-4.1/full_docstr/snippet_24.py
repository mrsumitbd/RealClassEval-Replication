
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        # Windows absolute: C:\ or D:/, relative: .\ or ..\
        # Unix absolute: /, relative: ./ or ../
        win_abs = re.compile(r'^[a-zA-Z]:[\\/][^:*?"<>|]*')
        unix_abs = re.compile(r'^/[^:*?"<>|]*')
        rel = re.compile(r'^(\.{1,2}[\\/][^:*?"<>|]*)')
        # Exclude URLs
        if re.match(r'^[a-zA-Z]+://', path):
            return False
        if win_abs.match(path) or unix_abs.match(path) or rel.match(path):
            return True
        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        # Windows absolute: C:\path\to\file or C:/path/to/file
        win_abs = r'[a-zA-Z]:[\\/](?:[^\s:*?"<>|]+[\\/])*[^\s:*?"<>|]+'
        # Unix absolute: /path/to/file
        unix_abs = r'/(?:[^\s:*?"<>|/]+/)*[^\s:*?"<>|/]+'
        # Relative: ./path/to/file or ../path/to/file
        rel = r'\.{1,2}[\\/](?:[^\s:*?"<>|]+[\\/])*[^\s:*?"<>|]+'
        # Combine patterns
        pattern = f'({win_abs})|({unix_abs})|({rel})'
        # Exclude URLs
        url_pattern = re.compile(r'[a-zA-Z]+://[^\s]+')
        text_wo_urls = url_pattern.sub('', text)
        matches = re.findall(pattern, text_wo_urls)
        # Flatten and filter empty
        paths = [m for tup in matches for m in tup if m]
        return paths
