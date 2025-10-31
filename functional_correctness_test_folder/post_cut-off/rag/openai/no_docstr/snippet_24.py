
from typing import List
import re


class LocalPathExtractor:
    '''本地路径提取器'''

    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        if not isinstance(path, str):
            return False

        # 1. 绝对路径（Unix）
        if path.startswith('/'):
            return True

        # 2. 绝对路径（Windows）
        if re.match(r'^[a-zA-Z]:[\\/]', path):
            return True

        # 3. 相对路径（./ 或 ../ 或 直接文件名）
        if path.startswith('./') or path.startswith('../') or not path.startswith('.'):
            # 排除 URL
            if re.match(r'^[a-zA-Z]+://', path):
                return False
            return True

        # 4. file:// URI
        if path.startswith('file://'):
            return True

        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        if not isinstance(text, str):
            return []

        # 简单的路径匹配模式
        # 1. Windows 绝对路径：C:\path\to\file 或 C:/path/to/file
        # 2. Unix 绝对路径：/path/to/file
        # 3. 相对路径：./file 或 ../file 或 file
        # 4. file:// URI
        pattern = r'''
            (?<!\w)                                   # 前面不是单词字符
            (?:                                       # 路径前缀
                [a-zA-Z]:[\\/]|                       # Windows 绝对路径
                /|                                   # Unix 绝对路径
                \.{0,2}[\\/]|                        # ./ 或 ../
                file://                              # file URI
            )
            [^\s]+                                     # 路径主体（不含空白）
        '''
        matches = re.findall(pattern, text, re.VERBOSE)

        # 过滤掉 URL（http://, https://, ftp:// 等）
        local_paths = [
            m for m in matches if LocalPathExtractor.is_local_path(m)]

        return local_paths
