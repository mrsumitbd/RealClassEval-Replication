
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        # 简单的正则表达式来匹配本地路径
        return bool(re.match(r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$', path)) or \
            bool(
                re.match(r'^\/(?:[^\\/:*?"<>|\r\n]+\/)*[^\\/:*?"<>|\r\n]*$', path))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        # 提取Windows和Unix风格的本地路径
        windows_path_pattern = r'[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*'
        unix_path_pattern = r'\/(?:[^\\/:*?"<>|\r\n]+\/)*[^\\/:*?"<>|\r\n]*'
        combined_pattern = rf'({windows_path_pattern}|{unix_path_pattern})'
        return re.findall(combined_pattern, text)
