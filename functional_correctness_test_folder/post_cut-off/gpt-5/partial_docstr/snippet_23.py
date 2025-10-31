from typing import List, Optional
import re
from urllib.parse import urlparse


class GitHubURLExtractor:

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        if not text:
            return []

        patterns = [
            r'(?:https?://)github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?(?:/[^\s\]\)\}\'>"]*)?',
            r'git@github\.com:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?'
        ]

        urls: List[str] = []
        seen = set()

        for pat in patterns:
            for m in re.finditer(pat, text):
                url = m.group(0)

                # Trim trailing punctuation that often sticks to URLs in prose
                url = url.rstrip('.,;:!?)\]}\'"')

                if url not in seen:
                    seen.add(url)
                    urls.append(url)

        return urls

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        if not text:
            return None

        candidates: List[str] = []

        # 1) Quoted paths after common keywords
        patterns_quoted = [
            r'(?:目标路径|路径|目录|保存到|保存于|输出到|target\s*path|directory|folder|dir|path)\s*[:：]\s*["“](.+?)["”]',
            r'(?:to|到)\s*["“](.+?)["”]',
        ]

        # 2) Unquoted paths after common keywords (stop at whitespace or punctuation)
        patterns_unquoted = [
            r'(?:目标路径|路径|目录|保存到|保存于|输出到|target\s*path|directory|folder|dir|path)\s*[:：]\s*([^\s,;，；]+)',
            r'(?:to|到)\s*([^\s,;，；]+)',
        ]

        for pat in patterns_quoted:
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                candidates.append(m.group(1))

        if not candidates:
            for pat in patterns_unquoted:
                for m in re.finditer(pat, text, flags=re.IGNORECASE):
                    candidates.append(m.group(1))

        # Basic validation and cleanup
        def clean_path(p: str) -> str:
            p = p.strip().strip('"“”\'')
            p = p.rstrip('.,;:!?)\]}')
            return p

        def looks_like_path(p: str) -> bool:
            # Heuristics: contains slashes or starts with ./, ../, ~, or drive letter
            if not p:
                return False
            if p.startswith(("./", "../", "~", "/")):
                return True
            if re.match(r'^[A-Za-z]:[\\/]', p):
                return True
            if '/' in p or '\\' in p:
                return True
            return False

        for cand in candidates:
            cp = clean_path(cand)
            if looks_like_path(cp):
                return cp

        # As a fallback, if any candidate exists, return the first cleaned one
        if candidates:
            return clean_path(candidates[0])

        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        if not url:
            return ""

        url = url.strip()

        # SSH form: git@github.com:owner/repo(.git)?
        m = re.match(
            r'^git@github\.com:([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:\.git)?/?', url)
        if m:
            owner, repo = m.group(1), m.group(2)
            return f"{owner}/{repo}"

        # HTTPS/HTTP
        try:
            parsed = urlparse(url)
            if parsed.scheme in ('http', 'https') and parsed.netloc.endswith('github.com'):
                path = parsed.path.lstrip('/')
                parts = path.split('/')
                if len(parts) >= 2 and parts[0] and parts[1]:
                    owner = parts[0]
                    repo = parts[1]
                    repo = re.sub(r'\.git$', '', repo)
                    return f"{owner}/{repo}"
        except Exception:
            pass

        # Fallback: attempt to regex extract owner/repo anywhere in string pointing to github.com
        m2 = re.search(
            r'github\.com[:/]+([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)', url)
        if m2:
            owner, repo = m2.group(1), re.sub(r'\.git$', '', m2.group(2))
            return f"{owner}/{repo}"

        return ""
