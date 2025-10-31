import os
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''

    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        if not path:
            return False
        # Check for absolute paths (Unix and Windows)
        if os.path.isabs(path):
            return True
        # Check for relative paths (start with ./, ../, or .\ ..\)
        if path.startswith('./') or path.startswith('../') or path.startswith('.\\') or path.startswith('..\\'):
            return True
        # Windows drive letter
        if re.match(r'^[a-zA-Z]:[\\/]', path):
            return True
        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        # Regex for Unix and Windows paths
        # Matches: /home/user/file.txt, ./file.txt, ../file.txt, C:\Users\file.txt, D:/file.txt
        pattern = r'(?:(?:[a-zA-Z]:[\\/])|(?:\.\.?[\\/])|(?:/))[\w\-.\\/ ]+'
        matches = re.findall(pattern, text)
        # Remove trailing spaces and filter out non-paths
        paths = [m.strip()
                 for m in matches if LocalPathExtractor.is_local_path(m.strip())]
        return paths
