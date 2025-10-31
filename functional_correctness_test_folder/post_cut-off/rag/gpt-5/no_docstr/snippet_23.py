import re
from typing import List, Optional
from urllib.parse import urlparse


class GitHubURLExtractor:
    """提取GitHub URL的工具类"""

    _PUNCT_TRAIL = '.,;:)]}>\'"`'
    _PUNCT_LEAD = '<([\'"`'

    @staticmethod
    def _clean_url(url: str) -> str:
        url = url.strip()
        while url and url[0] in GitHubURLExtractor._PUNCT_LEAD:
            url = url[1:]
        while url and url[-1] in GitHubURLExtractor._PUNCT_TRAIL:
            url = url[:-1]
        return url

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """从文本中提取GitHub URLs"""
        if not text:
            return []

        patterns = [
            r'(?P<url>(?:https?://|git\+https://)github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?(?:/[^\s\)\]\}\>\"\'`#]*)?)',
            r'(?P<url>git@github\.com:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?(?:/[^\s\)\]\}\>\"\'`#]*)?)',
            r'(?P<url>https?://raw\.githubusercontent\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/[^\s\)\]\}\>\"\'`#]*)',
        ]
        seen = set()
        results: List[str] = []

        for pat in patterns:
            for m in re.finditer(pat, text):
                url = GitHubURLExtractor._clean_url(m.group('url'))
                if url and url not in seen:
                    seen.add(url)
                    results.append(url)

        return results

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """从文本中提取目标路径"""
        if not text:
            return None

        path_patterns = [
            r'(?:目标路径|目标目录)\s*[:：]\s*([^\s\n\r]+)',
            r'(?:target[_\s-]?path)\s*[:=]\s*([^\s\n\r]+)',
            r'(?:save\s+to|保存到)\s+([^\s\n\r]+)',
            r'(?:路径为|路径是)\s*([^\s\n\r]+)',
            r'(?:dest(?:ination)?|output[_\s-]?dir(?:ectory)?)\s*[:=]\s*([^\s\n\r]+)',
        ]

        for pat in path_patterns:
            m = re.search(pat, text, flags=re.IGNORECASE)
            if not m:
                continue
            candidate = m.group(1).strip().strip('\'"`')
            if candidate.lower().startswith(('http://', 'https://', 'git@', 'git+https://')):
                continue
            if candidate:
                return candidate

        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """从URL推断仓库名称"""
        if not url:
            return ''

        s = url.strip()

        if s.startswith('git@github.com:'):
            tail = s.split(':', 1)[1]
            parts = tail.split('/')
            if len(parts) >= 2:
                repo = parts[1]
                if repo.endswith('.git'):
                    repo = repo[:-4]
                repo = repo.split('#', 1)[0]
                repo = repo.split('?', 1)[0]
                return repo or ''

        if s.startswith('git+https://'):
            s = s[len('git+'):]

        parsed = urlparse(s)

        host = (parsed.netloc or '').lower()
        path = parsed.path or ''
        segments = [seg for seg in path.split('/') if seg]

        if host.endswith('github.com'):
            if len(segments) >= 2:
                repo = segments[1]
                if repo.endswith('.git'):
                    repo = repo[:-4]
                return repo or ''
            return ''

        if host == 'raw.githubusercontent.com':
            if len(segments) >= 2:
                return segments[1] or ''

        return ''
