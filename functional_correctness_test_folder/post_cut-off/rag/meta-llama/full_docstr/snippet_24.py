
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        # Windows and Linux/Unix path patterns
        patterns = [r'^[A-Z]:\\', r'^/[a-zA-Z0-9_/.-]+']
        for pattern in patterns:
            if re.match(pattern, path):
                return True
        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        # Regular expression pattern to match Windows and Linux/Unix paths
        pattern = r'([A-Z]:\\[^\s<>"]+|/[a-zA-Z0-9_/.-]+)'
        return re.findall(pattern, text)
