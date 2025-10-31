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
        # Check for absolute Unix or Windows path
        if os.path.isabs(path):
            return True
        # Check for relative path (starts with ./, ../, or .\ ..\)
        if path.startswith('./') or path.startswith('../') or path.startswith('.\\') or path.startswith('..\\'):
            return True
        # Check for Windows drive letter
        if re.match(r'^[a-zA-Z]:[\\/]', path):
            return True
        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        # Regex for Unix and Windows paths
        # Unix: /home/user/file.txt, ./file.txt, ../file.txt
        # Windows: C:\Users\file.txt, .\file.txt, ..\file.txt
        pattern = r'([a-zA-Z]:[\\/][\w\-.\\\/ ]+|(?:\.\.?[\\/])[\w\-.\\\/ ]+|\/[\w\-.\\\/ ]+)'
        matches = re.findall(pattern, text)
        # Filter out matches that are not local paths
        return [m for m in matches if LocalPathExtractor.is_local_path(m)]
