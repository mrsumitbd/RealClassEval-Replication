import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''

    # Precompiled regex patterns for unquoted paths (no spaces inside)
    _P_WIN_DRIVE = re.compile(r'(?<!\w)([a-zA-Z]:[\\/][^\s"\'<>|]+)')
    _P_UNC = re.compile(
        r'(?<!\w)(?:(?:\\\\|//)[^\s\\/]+[\\/][^\s"\'<>|]+(?:[\\/][^\s"\'<>|]+)*)')
    _P_POSIX_ABS = re.compile(r'(?<!\S)/(?!/)[^\s"\'<>|]+')
    _P_TILDE = re.compile(r'(?<!\S)~[\\/][^\s"\'<>|]+')
    _P_REL_DOT = re.compile(r'(?<!\S)\.{1,2}(?:[\\/][^\s"\'<>|]+)+')

    # Quoted strings ("..."/'...') – we'll validate content using is_local_path
    _P_QUOTED = re.compile(r'([\'"])(.+?)\1')

    # URL scheme detector
    _P_URL_SCHEME = re.compile(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://')

    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        if not isinstance(path, str):
            return False

        s = path.strip()

        # Strip wrapping quotes if any
        if len(s) >= 2 and ((s[0] == s[-1]) and s[0] in ('"', "'")):
            s = s[1:-1].strip()

        if not s:
            return False

        # Exclude URL-like strings
        if LocalPathExtractor._P_URL_SCHEME.match(s):
            return False

        # UNC path: \\server\share\... or //server/share/...
        if re.match(r'^(?:\\\\|//)[^\\/\r\n]+[\\/][^\\/\r\n]+(?:[\\/].*)?$', s):
            return True

        # Windows drive path: C:\..., C:/..., or bare drive "C:" (current-dir on drive)
        if re.match(r'^[a-zA-Z]:(?:[\\/].*)?$', s):
            return True

        # Windows root on current drive: \folder\... (single leading backslash)
        if re.match(r'^\\(?!\\).+', s):
            return True

        # POSIX absolute: /...
        if s.startswith('/'):
            return True

        # Home dir: ~ or ~/..., ~\...
        if s == '~' or s.startswith('~/') or s.startswith('~\\'):
            return True

        # Relative with dot: ., .., ./..., .\..., ../..., ..\...
        if s in ('.', '..'):
            return True
        if s.startswith('./') or s.startswith('.\\') or s.startswith('../') or s.startswith('..\\'):
            return True

        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        if not text:
            return []

        results: List[str] = []

        def add(path: str, quoted: bool = False):
            p = path
            # Trim trailing sentence punctuation for unquoted matches
            if not quoted:
                while p and p[-1] in '.,;:!?)]}':
                    p = p[:-1]
            if p and LocalPathExtractor.is_local_path(p):
                results.append(p)

        # 1) Extract quoted candidates and validate
        for m in LocalPathExtractor._P_QUOTED.finditer(text):
            content = m.group(2).strip()
            if content:
                add(content, quoted=True)

        # 2) Extract unquoted patterns
        for m in LocalPathExtractor._P_WIN_DRIVE.finditer(text):
            add(m.group(1), quoted=False)

        for m in LocalPathExtractor._P_UNC.finditer(text):
            add(m.group(0), quoted=False)

        for m in LocalPathExtractor._P_POSIX_ABS.finditer(text):
            add(m.group(0), quoted=False)

        for m in LocalPathExtractor._P_TILDE.finditer(text):
            add(m.group(0), quoted=False)

        for m in LocalPathExtractor._P_REL_DOT.finditer(text):
            add(m.group(0), quoted=False)

        return results
