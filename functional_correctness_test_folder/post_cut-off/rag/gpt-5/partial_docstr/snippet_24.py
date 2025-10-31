import re
from typing import List


class LocalPathExtractor:
    '''本地路径提取器'''

    # Patterns for validation (is_local_path)
    _URL_SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.\-]*://')
    _WIN_DRIVE_RE = re.compile(
        r'^[a-zA-Z]:[\\/](?:[^\\/:*?"<>|\r\n]+[\\/])*[^\\/:*?"<>|\r\n]*$')
    _UNC_RE = re.compile(
        r'^\\\\[^\\/\s]+[\\\/][^\\/\s]+(?:[\\\/][^\\\/:*?"<>|\r\n]+)*$')
    _UNIX_ABS_RE = re.compile(r'^/(?:[^\r\n]*)$')
    _REL_RE = re.compile(r'^\.(?:\.[\\/]|[\\/])[^\r\n]+$')
    _HOME_RE = re.compile(r'^~[\\/][^\r\n]*$')

    # Pattern for unquoted extraction (avoid whitespace inside)
    _UNQUOTED_EXTRACT_RE = re.compile(
        r'(?<![A-Za-z0-9_])('
        r'[A-Za-z]:[\\/](?:[^\\/:*?"<>|\s\r\n]+[\\/])*[^\\/:*?"<>|\s\r\n]*'
        r'|\\\\[^\\/\s]+[\\\/][^\\/\s]+(?:[\\\/][^\\\/:*?"<>|\s\r\n]+)*'
        r'|/(?:[^ \t\r\n/][^ \t\r\n]*)(?:/(?:[^ \t\r\n/][^ \t\r\n]*))*'
        r'|\.\.(?:[\\/][^ \t\r\n]+)+'
        r'|\.(?:[\\/][^ \t\r\n]+)+'
        r'|~[\\/][^ \t\r\n]+(?:[\\/][^ \t\r\n]+)*'
        r')'
    )

    # Pattern for quoted extraction
    _QUOTED_EXTRACT_RE = re.compile(r'(["\'])([^"\']+?)\1')

    @staticmethod
    def _clean_candidate(s: str) -> str:
        s = s.strip()
        # Strip surrounding quotes/brackets if paired
        pairs = {'"': '"', "'": "'", '(': ')', '[': ']', '{': '}'}
        if s and s[0] in pairs and s.endswith(pairs[s[0]]):
            s = s[1:-1].strip()
        # Strip trailing punctuation commonly attached in prose
        while s and s[-1] in '.,;:!?)\]}\'':
            s = s[:-1]
        # Strip leading opening punctuation if any leftover
        while s and s[0] in '(["\'':
            s = s[1:]
        return s.strip()

    @staticmethod
    def is_local_path(path: str) -> bool:
        '''判断是否为本地路径'''
        if not isinstance(path, str):
            return False
        s = LocalPathExtractor._clean_candidate(path)
        if not s:
            return False
        # Exclude URLs
        if LocalPathExtractor._URL_SCHEME_RE.match(s):
            return False
        # Exclude protocol-relative URLs
        if s.startswith('//'):
            return False
        # Validate against local path patterns
        if (LocalPathExtractor._WIN_DRIVE_RE.match(s) or
            LocalPathExtractor._UNC_RE.match(s) or
            LocalPathExtractor._UNIX_ABS_RE.match(s) or
            LocalPathExtractor._REL_RE.match(s) or
                LocalPathExtractor._HOME_RE.match(s)):
            return True
        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        '''从文本中提取本地文件路径'''
        if not isinstance(text, str) or not text:
            return []
        results: List[str] = []
        seen = set()

        def add_candidate(raw: str):
            cand = LocalPathExtractor._clean_candidate(raw)
            if not cand:
                return
            if LocalPathExtractor.is_local_path(cand) and cand not in seen:
                seen.add(cand)
                results.append(cand)

        # First, handle quoted paths (allowing spaces)
        for m in LocalPathExtractor._QUOTED_EXTRACT_RE.finditer(text):
            candidate = m.group(2).strip()
            add_candidate(candidate)

        # Then, handle unquoted paths
        for m in LocalPathExtractor._UNQUOTED_EXTRACT_RE.finditer(text):
            candidate = m.group(1)
            start = m.start(1)
            # Avoid capturing URL path part like http://example.com/path
            if candidate.startswith('/'):
                if start >= 3 and text[start-3:start] == '://':
                    continue
                if start >= 2 and text[start-2:start] == '//':
                    continue
            add_candidate(candidate)

        return results
