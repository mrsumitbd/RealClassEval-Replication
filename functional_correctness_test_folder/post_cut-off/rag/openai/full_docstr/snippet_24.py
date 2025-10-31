
import os
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''

    # 正则表达式匹配常见的本地文件路径（绝对路径和相对路径）
    _path_pattern = re.compile(
        r'''
        (?:
            # Windows 绝对路径，例如 C:\path\to\file
            (?:[a-zA-Z]:[\\/])?
            # Unix 绝对路径，例如 /path/to/file
            (?:[\\/])?
        )
        [^\s]+
        ''',
        re.VERBOSE
    )

    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        if not path:
            return False

        # 排除 URL
        if re.match(r'^[a-zA-Z]+://', path):
            return False

        # 绝对路径检查
        if os.path.isabs(path):
            return True

        # 以 . 或 .. 开头的相对路径
        if path.startswith('.') or path.startswith('~'):
            return True

        # Windows 相对路径（含反斜杠）
        if re.match(r'^[a-zA-Z]:[\\/]', path):
            return True

        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        if not text:
            return []

        # 找到所有可能的路径
        candidates = LocalPathExtractor._path_pattern.findall(text)

        # 过滤掉非本地路径
        local_paths = [
            p for p in candidates if LocalPathExtractor.is_local_path(p)]

        return local_paths
