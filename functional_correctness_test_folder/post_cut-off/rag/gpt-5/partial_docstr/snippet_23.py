import os
import re
from typing import List, Optional
from urllib.parse import urlparse


class GitHubURLExtractor:
    """提取GitHub URL的工具类"""

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """从文本中提取GitHub URLs"""
        if not text:
            return []

        patterns = [
            r'(?P<url>https?://(?:[\w.-]*github(?:usercontent)?\.com|gist\.github\.com)/[^\s"\'<>)\]]+)',
            r'(?P<url>git@github\.com:[^\s"\'<>)\]]+)',
        ]

        candidates: List[str] = []
        for pat in patterns:
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                candidates.append(m.group('url'))

        def clean(u: str) -> str:
            u = u.strip()
            # strip surrounding brackets/quotes if present
            if len(u) > 1 and u[0] in '([{\'''"' and u[-1] in ')]}\'''"':
                pairs = {'(': ')', '[': ']', '{': '}', '"': '"', "'": "'"}
                if pairs.get(u[0]) == u[-1]:
                    u = u[1:-1]
            # strip trailing punctuation commonly attached in prose
            while u and u[-1] in '.,;:!?)"]}':
                u = u[:-1]
            return u

        seen = set()
        result: List[str] = []
        for url in map(clean, candidates):
            if url and url not in seen:
                seen.add(url)
                result.append(url)
        return result

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """从文本中提取目标路径"""
        if not text:
            return None

        # Line-based labeled patterns like "目标路径: xxx"
        label_patterns = [
            r'^\s*(?:目标路径|路径|保存路径|存放目录|目录|输出目录|输出路径)\s*[:：]\s*(.+?)\s*$',
            r'^\s*(?:target\s*path|destination|dest(?:ination)?|dir(?:ectory)?|folder|path)\s*[:：]\s*(.+?)\s*$',
        ]
        # Verb phrases like "保存到 xxx", "save to xxx"
        action_patterns = [
            r'(?:保存到|存到|放到|存放至|输出到)\s+(.+)',
            r'(?:save\s+to|write\s+to|output\s+to|export\s+to)\s+(.+)',
        ]
        # CLI options like "--output out/dir" or "-o out/dir"
        option_patterns = [
            r'(?:^|\s)(?:-o|--output|--out|--dest(?:ination)?|--dir|--directory)\s+([^\s]+)',
        ]

        def clean_path(p: str) -> str:
            p = p.strip()
            # Remove inline trailing comments or punctuation
            p = re.split(r'\s+#', p, maxsplit=1)[0].strip()
            # Trim wrapping quotes/backticks
            if len(p) >= 2 and p[0] in ('"', "'", '`') and p[-1] == p[0]:
                p = p[1:-1]
            # Remove trailing punctuation not typical for paths
            while p and p[-1] in '.,;:!?)"]}':
                p = p[:-1]
            # Expand ~
            p = os.path.expanduser(p)
            return p

        # Check labeled lines first
        for line in text.splitlines():
            for pat in label_patterns:
                m = re.search(pat, line, flags=re.IGNORECASE)
                if m:
                    candidate = clean_path(m.group(1))
                    if candidate:
                        return candidate

        # Check action patterns line-wise
        for line in text.splitlines():
            for pat in action_patterns:
                m = re.search(pat, line, flags=re.IGNORECASE)
                if m:
                    candidate = clean_path(m.group(1))
                    if candidate:
                        return candidate

        # Check option patterns globally
        for pat in option_patterns:
            m = re.search(pat, text, flags=re.IGNORECASE | re.MULTILINE)
            if m:
                candidate = clean_path(m.group(1))
                if candidate:
                    return candidate

        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """从URL推断仓库名称"""
        if not url:
            return ''

        url = url.strip()

        # SSH format: git@github.com:owner/repo(.git)
        ssh_match = re.match(
            r'^git@github\.com:([^/\s]+)/([^/\s]+?)(?:\.git)?(?:[/\s].*)?$', url, flags=re.IGNORECASE)
        if ssh_match:
            repo = ssh_match.group(2)
            return re.sub(r'\.git$', '', repo, flags=re.IGNORECASE)

        # Parse HTTP(S) URLs
        try:
            parsed = urlparse(url)
        except Exception:
            return ''

        host = (parsed.netloc or '').lower()
        path = (parsed.path or '').strip('/')

        if not host and url.startswith('github.com/'):
            host = 'github.com'
            path = url[len('github.com/'):].strip('/')

        segments = [seg for seg in path.split('/') if seg]

        def strip_git(name: str) -> str:
            return re.sub(r'\.git$', '', name, flags=re.IGNORECASE)

        if not segments:
            return ''

        if host == 'github.com':
            if len(segments) >= 2:
                return strip_git(segments[1])
            return ''

        if host in ('raw.githubusercontent.com', 'codeload.github.com'):
            if len(segments) >= 2:
                return strip_git(segments[1])
            return ''

        if host == 'api.github.com':
            # e.g., /repos/owner/repo/...
            if len(segments) >= 3 and segments[0].lower() == 'repos':
                return strip_git(segments[2])
            return ''

        if host == 'gist.github.com':
            # Fallback to gist id or last segment
            return segments[-1] if segments else ''

        # Any other *.github.com subdomain: try owner/repo pattern
        if host.endswith('.github.com') and len(segments) >= 2:
            return strip_git(segments[1])

        return ''
