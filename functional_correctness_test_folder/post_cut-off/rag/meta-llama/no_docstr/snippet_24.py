
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        # Windows路径匹配规则
        windows_pattern = re.compile(r'^[A-Z]:\\.*$')
        # Linux路径匹配规则
        linux_pattern = re.compile(r'^/.*$')
        # 相对路径匹配规则
        relative_pattern = re.compile(r'^\.{1,2}/.*$')

        return bool(windows_pattern.match(path)) or bool(linux_pattern.match(path)) or bool(relative_pattern.match(path))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        # Windows路径匹配规则
        windows_pattern = re.compile(r'[A-Z]:\\[^\\:*?"<>|\r\n]+')
        # Linux路径匹配规则
        linux_pattern = re.compile(r'/[^/:*?"<>|\r\n]+')
        # 相对路径匹配规则
        relative_pattern = re.compile(r'\.{1,2}/[^:*?"<>|\r\n]+')

        windows_paths = windows_pattern.findall(text)
        linux_paths = linux_pattern.findall(text)
        relative_paths = relative_pattern.findall(text)

        paths = windows_paths + linux_paths + relative_paths
        # 过滤掉非路径字符串
        paths = [
            path for path in paths if LocalPathExtractor.is_local_path(path)]
        return paths
