
import re
from typing import List, Optional
from urllib.parse import urlparse


class GitHubURLExtractor:
    """提取GitHub URL的工具类"""

    # 正则匹配常见的 GitHub URL（https、ssh、git@）
    _URL_RE = re.compile(
        r"""
        (?:
            https?://github\.com/[^\s/]+/[^\s/]+(?:\.git)?   # https://github.com/user/repo(.git)?
            |
            git@github\.com:[^\s/]+/[^\s/]+(?:\.git)?        # git@github.com:user/repo(.git)?
            |
            ssh://git@github\.com/[^\s/]+/[^\s/]+(?:\.git)?  # ssh://git@github.com/user/repo(.git)?
        )
        """,
        re.VERBOSE,
    )

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """从文本中提取 GitHub URLs"""
        return GitHubURLExtractor._URL_RE.findall(text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """
        从文本中提取目标路径（URL 中仓库后面的路径）。

        只返回第一个匹配的路径，如果没有路径则返回 None。
        """
        urls = GitHubURLExtractor.extract_github_urls(text)
        if not urls:
            return None

        for url in urls:
            # 处理 https / ssh
            if url.startswith(("http://", "https://", "ssh://")):
                parsed = urlparse(url)
                # path 形如 /user/repo[/path/...]
                parts = [p for p in parsed.path.split("/") if p]
                if len(parts) > 2:
                    # parts[0] = user, parts[1] = repo, rest = path
                    return "/".join(parts[2:])
                continue

            # 处理 git@github.com:user/repo(.git)[/path/...]
            if url.startswith("git@"):
                # 去掉前缀
                after_at = url.split(":", 1)[1]
                parts = [p for p in after_at.split("/") if p]
                if len(parts) > 2:
                    return "/".join(parts[2:])
                continue

        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """
        从 URL 推断仓库名称（不含 .git 后缀）。

        支持 https、ssh、git@ 三种形式。
        """
        # 处理 https / ssh
        if url.startswith(("http://", "https://", "ssh://")):
            parsed = urlparse(url)
            parts = [p for p in parsed.path.split("/") if p]
            if len(parts) >= 2:
                repo = parts[1]
            else:
                repo = ""
        # 处理 git@github.com:user/repo(.git)
        elif url.startswith("git@"):
            after_at = url.split(":", 1)[1]
            parts = [p for p in after_at.split("/") if p]
            if len(parts) >= 2:
                repo = parts[1]
            else:
                repo = ""
        else:
            repo = ""

        # 去掉 .git 后缀
        if repo.endswith(".git"):
            repo = repo[:-4]
        return repo
