from typing import List
import re


class LocalPathExtractor:
    '''本地路径提取器'''

    _url_scheme_re = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*://')

    # Windows drive path, UNC path, Unix absolute, home, and dotted relative paths (without spaces)
    _win_drive_re = r'[A-Za-z]:[\\/](?:[^\\/:*?"<>|\s]+[\\/]?)*[^\\/:*?"<>|\s]*'
    _unc_re = r'\\\\[^\\/:*?"<>|\s]+\\[^\\/:*?"<>|\s]+(?:\\[^\\/:*?"<>|\s]+)*'
    _unix_abs_re = r'/(?:[^ \t\n\r\f\v\\:*?"<>|]+/)*[^ \t\n\r\f\v\\:*?"<>|]*'
    _home_re = r'~[\\/](?:[^ \t\n\r\f\v\\:*?"<>|]+[\\/]?)*[^ \t\n\r\f\v\\:*?"<>|]*'
    _rel_dot_re = r'\.{1,2}[\\/](?:[^ \t\n\r\f\v\\:*?"<>|]+[\\/]?)*[^ \t\n\r\f\v\\:*?"<>|]*'

    # Combined regex for extraction; avoid preceding scheme:// via negative lookbehind where possible
    _paths_re = re.compile(
        rf'(?<![a-zA-Z0-9+.-])(?:{_unc_re}|{_win_drive_re}|{_home_re}|{_rel_dot_re}|{_unix_abs_re})'
    )

    _trailing_punct = ')]},;:?!\'"。；，、：！？）】】》．．'
    _leading_punct = '([{"\'《【（'

    @staticmethod
    def is_local_path(path: str) -> bool:
        if not path or '\n' in path or '\r' in path:
            return False

        s = path.strip()

        # Reject URL-like schemes (http://, https://, file://, etc.)
        if LocalPathExtractor._url_scheme_re.match(s):
            return False

        # Windows drive path
        if re.match(r'^[A-Za-z]:[\\/]', s):
            return True

        # UNC path
        if re.match(r'^\\\\[^\\/:*?"<>|\s]+\\[^\\/:*?"<>|\s]+', s):
            return True

        # Home path
        if re.match(r'^~[\\/]', s):
            return True

        # Dotted relative path
        if re.match(r'^\.{1,2}[\\/]', s):
            return True

        # Unix absolute path
        if s.startswith('/'):
            return True

        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        if not text:
            return []

        results: List[str] = []

        for m in LocalPathExtractor._paths_re.finditer(text):
            candidate = m.group(0)

            # Trim surrounding quotes/brackets if present
            # Leading
            while candidate and candidate[0] in LocalPathExtractor._leading_punct:
                candidate = candidate[1:]
            # Trailing
            while candidate and candidate[-1] in LocalPathExtractor._trailing_punct:
                candidate = candidate[:-1]

            # Filter out false positives with scheme:// right before match
            start = m.start()
            prefix = text[max(0, start - 10):start]
            if re.search(r'[a-zA-Z][a-zA-Z0-9+.-]*://$', prefix):
                continue

            if candidate and LocalPathExtractor.is_local_path(candidate):
                results.append(candidate)

        return results
