
from typing import List
import re


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        # 简单的正则表达式来匹配常见的本地路径格式
        local_path_pattern = re.compile(r'^[a-zA-Z]:\\|^\./|^\.\.|^/')
        return bool(local_path_pattern.match(path))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        # 简单的正则表达式来匹配常见的本地路径格式
        local_path_pattern = re.compile(
            r'[a-zA-Z]:\\[^"\s]+|(\./|../)[^"\s]+|/[^"\s]+')
        return local_path_pattern.findall(text)
