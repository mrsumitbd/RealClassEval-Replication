
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        # Windows路径匹配规则
        windows_pattern = re.compile(r'^[a-zA-Z]:\\.*$')
        # Linux路径匹配规则
        linux_pattern = re.compile(r'^(/[^/]+)+/?$')
        # 相对路径匹配规则
        relative_pattern = re.compile(r'^\.{1,2}(/.*)?$')

        return bool(windows_pattern.match(path)) or bool(linux_pattern.match(path)) or bool(relative_pattern.match(path))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        # 匹配Windows和Linux风格的路径
        pattern = re.compile(r'([a-zA-Z]:\\[^ ]+|(/[^ ]+)+|\.{1,2}(/[^ ]+)*)')
        paths = pattern.findall(text)
        # flatten the list
        paths = [
            path for path in paths if LocalPathExtractor.is_local_path(path)]
        return paths
