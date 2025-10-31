from typing import List, Optional
import re
from urllib.parse import urlparse


class GitHubURLExtractor:
    '''提取GitHub URL的工具类'''

    _URL_TRAILING_STRIP = '.,);:!?"\''

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        '''从文本中提取GitHub URLs'''
        if not text:
            return []

        patterns = [
            r'https?://(?:www\.)?github\.com/[^\s<>\[\]\(\)\'"]+',
            r'https?://raw\.githubusercontent\.com/[^\s<>\[\]\(\)\'"]+',
            r'https?://gist\.github\.com/[^\s<>\[\]\(\)\'"]+',
            r'ssh://git@github\.com/[^\s<>\[\]\(\)\'"]+',
            r'git@github\.com:[^\s<>\[\]\(\)\'"]+',
        ]

        urls: List[str] = []
        seen = set()

        for pat in patterns:
            for m in re.finditer(pat, text):
                url = m.group(0).strip()
                url = url.rstrip(GitHubURLExtractor._URL_TRAILING_STRIP)
                if url not in seen:
                    seen.add(url)
                    urls.append(url)

        return urls

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        if not text:
            return None

        # 1) 明确的提示短语
        hint_patterns = [
            r'(?:目标路径|路径|保存到|保存至|位置|输出到|target path|save to|path)\s*[:：]\s*([^\s,;]+)',
            r'(?:到|至)\s*([A-Za-z]:\\[^\s,;]+|/[^,\s;]+|\.(?:/|\\)[^\s,;]+)',
        ]
        for pat in hint_patterns:
            m = re.search(pat, text, flags=re.IGNORECASE)
            if m:
                return m.group(1).strip().strip('\'"')

        # 2) 代码块或反引号中的路径
        code_like = re.findall(r'`([^`]+)`', text)
        for token in code_like:
            tok = token.strip().strip('\'"')
            if GitHubURLExtractor._looks_like_path(tok):
                return tok

        # 3) 常见路径样式扫描
        generic_patterns = [
            r'([A-Za-z]:\\[^:\n\r\t,;]+)',          # Windows 绝对路径
            r'(/[^:\n\r\t,;]+)',                    # Unix 绝对路径
            r'(\.(?:/|\\)[^:\n\r\t,;]+)',           # 相对路径 ./ 或 .\
            r'(\.\.(?:/|\\)[^:\n\r\t,;]+)',         # 相对路径 ../ 或 ..\
        ]
        for pat in generic_patterns:
            m = re.search(pat, text)
            if m:
                return m.group(1).strip().strip('\'"')

        return None

    @staticmethod
    def _looks_like_path(s: str) -> bool:
        # 简单启发式判断
        if re.match(r'^[A-Za-z]:\\', s):  # Windows
            return True
        if s.startswith('/') or s.startswith('./') or s.startswith('../'):
            return True
        if '\\' in s or '/' in s:
            # 具有分隔符且不太像 URL
            if not re.match(r'^[a-z]+://', s):
                return True
        return False

    @staticmethod
    def infer_repo_name(url: str) -> str:
        '''从URL推断仓库名称'''
        if not url:
            return ''

        u = url.strip()

        # SSH: git@github.com:owner/repo.git
        m = re.match(r'^git@github\.com:([^/\s]+)/([^/\s]+)(?:/(.*))?$', u)
        if m:
            repo = m.group(2)
            return GitHubURLExtractor._clean_repo(repo)

        # SSH over scheme: ssh://git@github.com/owner/repo.git
        m = re.match(r'^ssh://git@github\.com/([^/\s]+)/([^/\s]+)(?:/.*)?$', u)
        if m:
            repo = m.group(2)
            return GitHubURLExtractor._clean_repo(repo)

        # HTTP(S)
        if re.match(r'^[a-z]+://', u):
            parsed = urlparse(u)
            host = (parsed.netloc or '').lower()

            path = parsed.path.strip('/')
            parts = [p for p in path.split('/') if p]

            # github.com/owner/repo/...
            if host.endswith('github.com'):
                # Exclude gist
                if host.startswith('gist.'):
                    return ''
                if len(parts) >= 2:
                    repo = parts[1]
                    return GitHubURLExtractor._clean_repo(repo)
                return ''

            # raw.githubusercontent.com/owner/repo/branch/...
            if host == 'raw.githubusercontent.com':
                if len(parts) >= 2:
                    repo = parts[1]
                    return GitHubURLExtractor._clean_repo(repo)
                return ''

        return ''

    @staticmethod
    def _clean_repo(repo: str) -> str:
        repo = repo.strip()
        if repo.endswith('.git'):
            repo = repo[:-4]
        return repo.strip()
