import os
import re
from typing import List, Optional
from urllib.parse import urlparse


class GitHubURLExtractor:
    """提取GitHub URL的工具类"""

    _TRAILING_CHARS = '.,;:!?)]}>"\''

    @staticmethod
    def _clean_url(u: str) -> str:
        u = u.strip()
        while u and u[-1] in GitHubURLExtractor._TRAILING_CHARS:
            u = u[:-1]
        return u

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """从文本中提取GitHub URLs"""
        if not text:
            return []
        patterns = [
            r'(https?://(?:[\w.-]*github(?:usercontent)?\.com)/[^\s<>"\'\]\)}]+)',
            r'(https?://(?:api|codeload)\.github\.com/[^\s<>"\'\]\)}]+)',
            r'(ssh://git@github\.com/[^\s<>"\'\]\)}]+)',
            r'(git@github\.com:[\w.\-]+/[\w.\-]+(?:\.git)?)',
            r'(?<!\w)(?:www\.)?github\.com/[^\s<>"\'\]\)}]+',  # schemeless
        ]
        urls: List[str] = []
        seen = set()
        for pat in patterns:
            for match in re.findall(pat, text, flags=re.IGNORECASE):
                url = GitHubURLExtractor._clean_url(match)
                # normalize schemeless to https
                if url.startswith('github.com/'):
                    url = 'https://' + url
                if url.startswith('www.github.com/'):
                    url = 'https://' + url
                if url and url not in seen:
                    seen.add(url)
                    urls.append(url)
        return urls

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """从文本中提取目标路径"""
        if not text:
            return None
        patterns = [
            r'(?:目标路径|保存路径|输出路径|目标目录|目录|路径|path|target(?:_path)?)\s*[:：]\s*([^\s,，。；;\n\r]+)',
            r'(?:保存到|输出到|保存于|输出于)\s+([^\s,，。；;\n\r]+)',
            r'(?:dest(?:ination)?|output|outdir)\s*[:=]\s*([^\s,，。；;\n\r]+)',
            r'\bto\s*=\s*([^\s,，。；;\n\r]+)',
        ]
        for pat in patterns:
            m = re.search(pat, text, flags=re.IGNORECASE)
            if m:
                path = m.group(1).strip().strip('\'"`“”‘’').rstrip(
                    GitHubURLExtractor._TRAILING_CHARS)
                if path:
                    path = os.path.expandvars(os.path.expanduser(path))
                    return path
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """从URL推断仓库名称"""
        if not url:
            return ''
        url = GitHubURLExtractor._clean_url(url)

        # SCP-like SSH form: git@github.com:owner/repo(.git)
        m = re.match(r'^\w+@github\.com:([^#?\s]+)', url, flags=re.IGNORECASE)
        if m:
            path = m.group(1).split('?', 1)[0].split('#', 1)[0].strip('/')
            parts = path.split('/')
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
                if repo.endswith('.git'):
                    repo = repo[:-4]
                return f'{owner}/{repo}'

        # Ensure scheme for schemeless urls like github.com/owner/repo
        parsed = urlparse(url if re.match(
            r'^[a-z]+://', url, re.I) else f'https://{url}')
        host = parsed.netloc.lower()
        parts = [p for p in parsed.path.split('/') if p]

        owner = repo = None
        if host == 'github.com' or host.endswith('.github.com'):
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
        elif host == 'api.github.com':
            if len(parts) >= 3 and parts[0].lower() == 'repos':
                owner, repo = parts[1], parts[2]
        elif host.endswith('githubusercontent.com'):
            # raw.githubusercontent.com/{owner}/{repo}/...
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
        elif host == 'codeload.github.com':
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
        elif host == 'gist.github.com':
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]

        if owner and repo:
            if repo.endswith('.git'):
                repo = repo[:-4]
            return f'{owner}/{repo}'
        return ''
