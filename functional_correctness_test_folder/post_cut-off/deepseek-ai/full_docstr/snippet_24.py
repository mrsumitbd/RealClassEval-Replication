
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        return path.startswith(('file://', '/', './', '../', '~/', 'C:\\', 'D:\\', 'E:\\'))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        pattern = r'(?:file://)?(?:[a-zA-Z]:)?(?:[\\/][^\\/:\*\?"<>\|\r\n]+)+[\\/]?'
        matches = re.finditer(pattern, text)
        paths = [match.group() for match in matches]
        return [path for path in paths if LocalPathExtractor.is_local_path(path)]
