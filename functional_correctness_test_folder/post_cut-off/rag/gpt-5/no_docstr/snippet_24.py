import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''

    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        if not path or not isinstance(path, str):
            return False

        s = path.strip()

        # 排除 URL/URI（包括 file://）
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.\-]*://', s):
            return False

        # Windows 盘符绝对路径: C:\ 或 C:/
        if re.match(r'^[A-Za-z]:[\\/]', s):
            return True

        # Windows UNC 路径: \\server\share 或 //server/share
        if re.match(r'^(?:\\\\|//)[^\\/\s]+[\\/][^\\/\s]+', s):
            return True

        # Unix 绝对路径: /...
        if s.startswith('/'):
            return True

        # 用户目录: ~ 或 ~user
        if s.startswith('~'):
            return True

        # 相对路径: ./ ../ .\ ..\
        if s.startswith('./') or s.startswith('../') or s.startswith('.\\') or s.startswith('..\\'):
            return True

        # 包含路径分隔符的相对路径（且不是 URL）
        if ('/' in s or '\\' in s) and '://' not in s:
            return True

        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        if not text:
            return []

        # 组合匹配模式，尽量宽松，之后用 is_local_path 进行过滤
        pattern = re.compile(
            r'''
            (
                [A-Za-z]:[\\/][^\s"'<>|()\[\]{}]*                  # Windows 盘符绝对路径
              | (?:\\\\|//)[^\\/\s]+[\\/][^\s"'<>|()\[\]{}]*       # Windows UNC 路径
              | ~[^\s"'<>|()\[\]{}]*                               # 用户目录路径
              | /[^\s"'<>|()\[\]{}]*                               # Unix 绝对路径
              | \.{1,2}[\\/][^\s"'<>|()\[\]{}]*                    # 点相对路径
              | (?:[^\s:/"'<>|()\[\]{}]+[\\/])+(?:[^\s"'<>|()\[\]{}]+)?  # 含分隔符的相对路径
            )
            ''',
            re.VERBOSE
        )

        candidates: List[str] = []
        seen = set()

        for m in pattern.finditer(text):
            candidate = m.group(0)

            # 去除末尾常见分隔标点，但保留中间的点号及扩展名
            while candidate and candidate[-1] in '.,;:!?)]}':
                candidate = candidate[:-1]

            # 去除起始的左括号等
            while candidate and candidate[0] in '([{':
                candidate = candidate[1:]

            if not candidate:
                continue

            if LocalPathExtractor.is_local_path(candidate):
                if candidate not in seen:
                    seen.add(candidate)
                    candidates.append(candidate)

        return candidates
