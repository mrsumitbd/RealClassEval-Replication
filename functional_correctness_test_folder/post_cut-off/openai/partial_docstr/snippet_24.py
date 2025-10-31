
import re
from typing import List
from urllib.parse import urlparse


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        """
        判断给定的路径字符串是否为本地路径。
        本地路径定义为：
        - 以文件协议(file://)开头的路径
        - 或者没有协议（scheme）且不以 http/https/ftp 等网络协议开头
        """
        if not path:
            return False
        parsed = urlparse(path)
        # 如果有 scheme 且不是 file，则不是本地路径
        if parsed.scheme and parsed.scheme.lower() != 'file':
            return False
        # 进一步排除以 http/https/ftp 开头的字符串
        if re.match(r'^(?:http|https|ftp)://', path, re.IGNORECASE):
            return False
        return True

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        """
        从文本中提取所有本地路径。
        支持常见的 Windows 和 Unix 路径格式。
        """
        if not text:
            return []

        # 正则匹配 Windows 路径（C:\path 或 C:/path）
        win_path_pattern = r'(?:[A-Za-z]:[\\/]|\\\\)[^\s]+'
        # Unix 路径（/path 或 ./path 或 ../path）
        unix_path_pattern = r'(?:\/|\.{1,2}[\\/])[^\\s]+'
        # 组合模式
        pattern = f'{win_path_pattern}|{unix_path_pattern}'

        candidates = re.findall(pattern, text)
        # 过滤掉包含网络协议的路径
        local_paths = [
            p for p in candidates if LocalPathExtractor.is_local_path(p)]
        return local_paths
