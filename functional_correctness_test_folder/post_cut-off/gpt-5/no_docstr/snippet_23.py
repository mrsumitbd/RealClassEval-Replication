from typing import List, Optional
import re
from urllib.parse import urlparse


class GitHubURLExtractor:

    @staticmethod
    def _strip_trailing_punct(s: str) -> str:
        # Strip common trailing punctuation that often follows inline URLs
        return s.rstrip('.,;:!?)"]}\'')

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        if not text:
            return []

        urls: List[str] = []
        seen = set()

        # Match https/http GitHub URLs (stop at whitespace or closing punctuation)
        http_pattern = re.compile(
            r"""(?P<url>https?://(?:www\.)?github\.com/[^\s<>\]\)}'"]+)""",
            re.IGNORECASE,
        )
        # Match git protocol URLs
        git_proto_pattern = re.compile(
            r"""(?P<url>git://github\.com/[^\s<>\]\)}'"]+)""",
            re.IGNORECASE,
        )
        # Match SSH shorthand URLs
        ssh_pattern = re.compile(
            r"""(?P<url>git@github\.com:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?)""",
            re.IGNORECASE,
        )

        for pat in (http_pattern, git_proto_pattern, ssh_pattern):
            for m in pat.finditer(text):
                raw = m.group("url")
                cleaned = GitHubURLExtractor._strip_trailing_punct(raw)
                if cleaned not in seen:
                    seen.add(cleaned)
                    urls.append(cleaned)

        return urls

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        urls = GitHubURLExtractor.extract_github_urls(text)
        for u in urls:
            repo = GitHubURLExtractor.infer_repo_name(u)
            if repo:
                return repo

        # Fallback: try plain owner/repo in text
        plain_pattern = re.compile(
            r"""(?<![\w.-])([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?![\w.-])"""
        )
        m = plain_pattern.search(text or "")
        if m:
            return f"{m.group(1)}/{m.group(2)}"
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        if not url:
            return ""

        # SSH: git@github.com:owner/repo(.git)
        m_ssh = re.match(
            r"""^git@github\.com:([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:\.git)?$""",
            url.strip(),
            re.IGNORECASE,
        )
        if m_ssh:
            owner, repo = m_ssh.group(1), m_ssh.group(2)
            return f"{owner}/{repo}"

        # git protocol: git://github.com/owner/repo(.git)(/...)
        m_git_proto = re.match(
            r"""^git://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:\.git)?(?:[/#?].*)?$""",
            url.strip(),
            re.IGNORECASE,
        )
        if m_git_proto:
            return f"{m_git_proto.group(1)}/{m_git_proto.group(2)}"

        # http(s) URLs
        try:
            parsed = urlparse(url.strip())
        except Exception:
            parsed = None

        if parsed and parsed.netloc:
            host = parsed.netloc.lower()
            if host.endswith("github.com"):
                # Remove leading slash and split
                path = parsed.path.lstrip("/")
                parts = [p for p in path.split("/") if p]
                if len(parts) >= 2:
                    owner = parts[0]
                    repo = parts[1]
                    if repo.endswith(".git"):
                        repo = repo[:-4]
                    return f"{owner}/{repo}"

        return ""
