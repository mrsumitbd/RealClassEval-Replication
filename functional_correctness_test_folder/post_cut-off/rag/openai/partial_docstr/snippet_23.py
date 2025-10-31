
import re
from typing import List, Optional
from urllib.parse import urlparse


class GitHubURLExtractor:
    """提取GitHub URL的工具类"""

    # 正则匹配 GitHub 的完整 URL，支持可选的 .git 后缀和后续路径
    _GITHUB_URL_RE = re.compile(
        r"https?://github\.com/(?P<owner>[^/\s]+)/(?P<repo>[^/\s]+)(?P<path>/[^?\s]*)?",
        re.IGNORECASE,
    )

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """从文本中提取 GitHub URLs"""
        if not text:
            return []

        matches = GitHubURLExtractor._GITHUB_URL_RE.findall(text)
        # 重新构造完整 URL
        urls = []
        for match in matches:
            owner, repo, path = match
            url = f"https://github.com/{owner}/{repo}"
            if path:
                url += path
            urls.append(url)
        return urls

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """
        从文本中提取目标路径（即 URL 中仓库后面的路径部分）。
        只返回第一个匹配的路径。
        """
        if not text:
            return None

        match = GitHubURLExtractor._GITHUB_URL_RE.search(text)
        if not match:
            return None

        path = match.group("path")
        return path if path else None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """
        从 URL 推断仓库名称（即 owner/repo）。
        如果 URL 无法解析，返回空字符串。
        """
        if not url:
            return ""

        try:
            parsed = urlparse(url)
            if parsed.netloc.lower() != "github.com":
                return ""

            # 去掉可能的 .git 后缀
            path_parts = [p for p in parsed.path.split("/") if p]
            if len(path_parts) < 2:
                return ""

            owner, repo = path_parts[0], path_parts[1]
            if repo.endswith(".git"):
                repo = repo[:-4]
            return f"{owner}/{repo}"
        except Exception:
            return ""
