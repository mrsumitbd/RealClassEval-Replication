
import re
from typing import List, Optional
from urllib.parse import urlparse


class GitHubURLExtractor:
    """提取GitHub URL的工具类"""

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """
        从文本中提取 GitHub URLs。

        支持的 URL 形式：
            - https://github.com/owner/repo
            - https://github.com/owner/repo.git
            - http://github.com/owner/repo
            - http://github.com/owner/repo.git
            - github.com/owner/repo
            - github.com/owner/repo.git
        """
        # 先把可能的 http/https 前缀去掉，统一处理
        pattern = re.compile(
            r"""
            (?:(?:https?://)?          # http:// 或 https:// 可选
            (?:www\.)?                 # www. 可选
            github\.com/               # github.com/
            [A-Za-z0-9_.-]+/           # owner
            [A-Za-z0-9_.-]+            # repo
            (?:\.git)?                 # .git 可选
            )
            """,
            re.VERBOSE | re.IGNORECASE,
        )
        matches = pattern.findall(text)
        # 去重并保持原始顺序
        seen = set()
        urls = []
        for m in matches:
            if m not in seen:
                seen.add(m)
                urls.append(m)
        return urls

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """
        从文本中提取目标路径。

        目标路径的常见写法：
            - target: /path/to/dir
            - target = /path/to/dir
            - path: /path/to/dir
            - path = /path/to/dir
        只返回第一个匹配的路径。
        """
        pattern = re.compile(
            r"""
            (?:target|path)          # target 或 path
            \s*[:=]\s*               # : 或 =，可有空格
            (?P<path>[^ \t\r\n]+)    # 路径（不含空白）
            """,
            re.VERBOSE | re.IGNORECASE,
        )
        match = pattern.search(text)
        return match.group("path") if match else None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """
        从 GitHub URL 推断仓库名称。

        例子：
            https://github.com/owner/repo.git  -> repo
            https://github.com/owner/repo      -> repo
            github.com/owner/repo.git          -> repo
        """
        # 解析 URL，去掉协议和 www
        parsed = urlparse(url if "://" in url else f"https://{url}")
        path = parsed.path  # /owner/repo or /owner/repo.git
        if not path:
            return ""
        # 去掉首尾斜杠
        path = path.strip("/")
        parts = path.split("/")
        if not parts:
            return ""
        repo = parts[-1]
        if repo.endswith(".git"):
            repo = repo[:-4]
        return repo
