
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        # 使用正则表达式匹配常见的本地路径模式
        pattern = r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$|^/(?:[^/]+/)*[^/]*$'
        return bool(re.match(pattern, path))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        # 使用正则表达式匹配文本中的本地路径
        pattern = r'[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*|/(?:[^/]+/)*[^/]*'
        matches = re.findall(pattern, text)
        # 过滤掉不符合本地路径规则的匹配项
        return [match for match in matches if LocalPathExtractor.is_local_path(match)]
