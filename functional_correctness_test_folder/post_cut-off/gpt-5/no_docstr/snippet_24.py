from typing import List
import re


class LocalPathExtractor:
    _url_scheme_re = re.compile(r'[a-zA-Z][a-zA-Z0-9+.\-]*://$')

    _path_re = re.compile(
        r'''
        (?:
            # Windows drive path: C:\dir\file or C:/dir/file
            (?P<win_drive>
                [A-Za-z]:[\\/](?:[^<>:"|?*\r\n]+[\\/])*[^<>:"|?*\r\n]*
            )
            |
            # UNC path: \\server\share\path or //server/share/path
            (?P<unc>
                (?:\\\\|//)[^\\/\s]+[\\/][^\\/\s]+(?:[\\/][^<>:"|?*\r\n]+)*
            )
            |
            # Unix absolute: /usr/local/bin or similar (no whitespace)
            (?P<unix_abs>
                /(?:[^\s/]+/)*[^\s/]*
            )
            |
            # Home path: ~/dir/file
            (?P<home>
                ~(?:/[^\s]+)*
            )
            |
            # Relative paths: ./dir/file, ../dir, dir/subdir/file (no colon to avoid schemes)
            (?P<rel>
                (?:\.{1,2}[\\/][^\s]+)
                |
                (?:[^\s:][^\s:]*[\\/][^\s]+)
            )
        )
        ''',
        re.VERBOSE
    )

    @staticmethod
    def _strip_wrapping_and_trailing(s: str) -> str:
        s = s.strip()
        if len(s) >= 2 and ((s[0] == s[-1] and s[0] in ('"', "'")) or (s[0] == '<' and s[-1] == '>')):
            s = s[1:-1].strip()
        # Strip common trailing punctuation that often follows inline paths
        while s and s[-1] in '.,;:)]}>\''"':
            s = s[:-1]
        return s

    @staticmethod
    def _looks_like_url_context(text: str, start: int) -> bool:
        # Check if characters immediately before start form a scheme://
        prefix = text[max(0, start - 32):start]
        return bool(LocalPathExtractor._url_scheme_re.search(prefix))

    @staticmethod
    def is_local_path(path: str) -> bool:
        if path is None:
            return False
        s = LocalPathExtractor._strip_wrapping_and_trailing(path)
        if not s:
            return False
        # If it contains a URL scheme, reject
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.\-]*://', s):
            return False
        m = LocalPathExtractor._path_re.fullmatch(s)
        return m is not None

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        if not text:
            return []
        results: List[str] = []
        seen = set()
        for m in LocalPathExtractor._path_re.finditer(text):
            s = m.group(0)
            start = m.start()
            # Avoid matches that are part of URL scheme contexts
            if LocalPathExtractor._looks_like_url_context(text, start):
                continue
            cleaned = LocalPathExtractor._strip_wrapping_and_trailing(s)
            if not cleaned:
                continue
            # Re-validate cleaned candidate as a full path pattern
            if not LocalPathExtractor._path_re.fullmatch(cleaned):
                continue
            # Exclude pure "http/" like artifacts
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.\-]*/$', cleaned):
                continue
            if cleaned not in seen:
                seen.add(cleaned)
                results.append(cleaned)
        return results
