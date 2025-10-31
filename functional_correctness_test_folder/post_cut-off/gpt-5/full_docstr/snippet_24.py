from typing import List
import re


class LocalPathExtractor:
    '''本地路径提取器'''

    # URL 模式，用于屏蔽文本中的 URL，避免被误识别为本地路径
    _URL_PATTERN = re.compile(r'\b[a-zA-Z][a-zA-Z0-9+.-]*://[^\s)\]\}>]+')

    # 各类本地路径正则
    _WIN_DRIVE = r'[A-Za-z]:[\\/](?:[^:*?"<>|\r\n]+[\\/]?)*[^:*?"<>|\r\n]*'
    _WIN_UNC = r'\\\\[^\\/:*?"<>|\r\n]+[\\\/][^\\/:*?"<>|\r\n]+(?:[\\\/][^\\/:*?"<>|\r\n]+)*'
    _WIN_REL = r'(?:\.\.?)[\\\/][^:*?"<>|\r\n]+(?:[\\\/][^:*?"<>|\r\n]+)*'
    _UNIX_ABS = r'/(?:[^/\s\r\n]+/)*[^/\s\r\n]*'
    _UNIX_REL = r'(?:\.\.?)/[^/\s\r\n]+(?:/[^/\s\r\n]+)*'

    # 组合路径模式，使用前瞻避免结尾带上标点和引号等
    _PATH_PATTERN = re.compile(
        r'('
        + _WIN_DRIVE + r'|'
        + _WIN_UNC + r'|'
        + _WIN_REL + r'|'
        + _UNIX_ABS + r'|'
        + _UNIX_REL +
        r')(?=$|[\s,;:!?，。．、)"\'\]]+)',
        re.UNICODE
    )

    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        if not path or not isinstance(path, str):
            return False
        # 排除 URL
        if LocalPathExtractor._URL_PATTERN.fullmatch(path):
            return False
        return bool(LocalPathExtractor._PATH_PATTERN.fullmatch(path))

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        if not text or not isinstance(text, str):
            return []

        # 屏蔽 URL，防止把 URL 中的路径片段误识别为本地路径
        masked = LocalPathExtractor._URL_PATTERN.sub(
            lambda m: ' ' * (m.end() - m.start()), text)

        results: List[str] = []
        seen = set()

        for m in LocalPathExtractor._PATH_PATTERN.finditer(masked):
            path = text[m.start():m.end()]
            # 去除尾随常见标点（保险处理，如极端情况下未被前瞻阻止）
            path = path.rstrip(' ,;:!?，。．、)"\']')
            if path and path not in seen:
                seen.add(path)
                results.append(path)

        return results
