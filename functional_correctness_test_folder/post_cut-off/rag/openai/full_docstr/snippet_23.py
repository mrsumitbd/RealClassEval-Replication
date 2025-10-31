
import re
from typing import List, Optional
from urllib.parse import urlparse


class GitHubURLExtractor:
    """提取GitHub URL的工具类"""

    # 正则匹配 GitHub 的 URL
    _GITHUB_URL_RE = re.compile(
        r"""
        (?P<url>
            https?://
            (?:www\.)?github\.com/
            [A-Za-z0-9_.-]+          # 用户名
            /
            [A-Za-z0-9_.-]+          # 仓库名
            (?:/[^ \t\n\r\f\v]*)?    # 可选路径
        )
        """,
        re.VERBOSE | re.IGNORECASE,
    )

    # 匹配 tree 或 blob 后的路径
    _TARGET_PATH_RE = re.compile(
        r"""
        (?:tree|blob)/          # tree 或 blob
        [^ \t\n\r\f\v/]+        # 分支名
        /                       # 路径分隔符
        (?P<path>[^ \t\n\r\f\v]+)   # 路径
        """,
        re.VERBOSE,
    )

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """从文本中提取 GitHub URLs"""
        if not text:
            return []

        urls = []
        for match in GitHubURLExtractor._GITHUB_URL_RE.finditer(text):
            url = match.group("url")
            # 去掉末尾的空格或换行
            url = url.rstrip(" \t\n\r\f\v")
            urls.append(url)
        return urls

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """
        从文本中提取目标路径（即 tree 或 blob 后的路径）。
        只返回第一个匹配的路径。
        """
        if not text:
            return None

        match = GitHubURLExtractor._TARGET_PATH_RE.search(text)
        if match:
            return match.group("path")
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """
        从 URL 推断仓库名称（即路径中的第二段）。
        例如：
            https://github.com/user/repo          -> repo
            https://github.com/user/repo/tree/... -> repo
        """
        if not url:
            return ""

        parsed = urlparse(url)
        # 解析路径，去掉首尾斜杠
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) >= 2:
            return parts[1]
        return ""
