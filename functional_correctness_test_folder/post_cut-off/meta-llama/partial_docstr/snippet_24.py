
import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''
    @staticmethod
    def is_local_path(path: str) -> bool:
        # Windows路径匹配规则
        windows_pattern = re.compile(r'^[a-zA-Z]:\\.*$')
        # Linux路径匹配规则
        linux_pattern = re.compile(r'^/.*$')
        # 相对路径匹配规则
        relative_pattern = re.compile(r'^\.{1,2}/.*$')

        return bool(windows_pattern.match(path)) or bool(linux_pattern.match(path)) or bool(relative_pattern.match(path))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        # 匹配Windows路径
        windows_pattern = re.compile(
            r'[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*')
        # 匹配Linux路径
        linux_pattern = re.compile(r'/(?:[^/\0]+/)*[^/\0]*')
        # 匹配相对路径
        relative_pattern = re.compile(r'\.{1,2}/(?:[^/\0]+/)*[^/\0]*')

        windows_paths = windows_pattern.findall(text)
        linux_paths = linux_pattern.findall(text)
        relative_paths = relative_pattern.findall(text)

        local_paths = windows_paths + linux_paths + relative_paths
        # 过滤掉非路径字符串
        local_paths = [
            path for path in local_paths if LocalPathExtractor.is_local_path(path)]

        return local_paths
