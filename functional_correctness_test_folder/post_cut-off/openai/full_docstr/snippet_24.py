
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''

    @staticmethod
    def is_local_path(path: str) -> bool:
        """
        判断是否为本地路径
        1. 以驱动器字母开头（Windows）如 C:\ 或 C:/ 。
        2. 以 / 开头（Unix/Linux/macOS） 。
        3. 以 . 或 .. 开头的相对路径。
        4. 不包含协议前缀（http://、https://、ftp:// 等）。
        """
        if not path:
            return False

        # 排除常见协议
        if re.match(r'^[a-zA-Z]+://', path):
            return False

        # Windows 驱动器路径
        if re.match(r'^[a-zA-Z]:[\\/]', path):
            return True

        # Unix 根路径
        if path.startswith('/'):
            return True

        # 相对路径
        if path.startswith('./') or path.startswith('../'):
            return True

        # 仅文件名（不含路径分隔符）
        if '/' not in path and '\\' not in path:
            return True

        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        """
        从文本中提取本地文件路径
        支持：
          - Windows 路径：C:\folder\file.txt 或 C:/folder/file.txt
          - Unix 路径：/usr/local/bin/script.sh
          - 相对路径：./file.txt 或 ../folder/file.txt
          - 仅文件名：file.txt
        """
        if not text:
            return []

        # 正则匹配可能的路径
        # 1. Windows 路径
        # 2. Unix 路径
        # 3. 相对路径
        # 4. 仅文件名（不含空格或分隔符）
        pattern = r'''
            (?:[a-zA-Z]:[\\/])?          # 可选驱动器
            (?:\.{1,2}[\\/])?            # 可选相对路径前缀
            (?:[^\s\\/]+[\\/])*          # 目录
            [^\s\\/]+                    # 文件名
        '''
        regex = re.compile(pattern, re.VERBOSE)

        matches = regex.findall(text)
        # 过滤掉非本地路径
        local_paths = [
            m for m in matches if LocalPathExtractor.is_local_path(m)]
        return local_paths
