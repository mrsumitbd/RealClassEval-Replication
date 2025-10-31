
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        # Check for common local path patterns (Windows and Unix-like)
        return (path.startswith(('./', '../', '/', '~/', 'C:\\', 'D:\\')) or
                re.match(r'^[A-Za-z]:\\', path) is not None)

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        # Regex pattern to match common local paths
        pattern = r'(?:\.{0,2}[\\/][^\s\\/]+(?:[\\/][^\s\\/]+)*)|(?:[A-Za-z]:\\[^\s\\]+(?:\\[^\s\\]+)*)|(?:~[\\/][^\s\\/]+(?:[\\/][^\s\\/]+)*)'
        matches = re.findall(pattern, text)
        return [match for match in matches if LocalPathExtractor.is_local_path(match)]
