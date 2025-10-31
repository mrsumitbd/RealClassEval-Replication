
import re
from typing import List, Optional


class GitHubURLExtractor:
    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """
        Extract all GitHub URLs from the given text.

        Supports:
        - HTTPS URLs: https://github.com/...
        - SSH URLs: git@github.com:...
        - Git protocol URLs: git://github.com/...
        """
        pattern = re.compile(
            r"""
            (?:https?://github\.com/|git@github\.com:|git://github\.com/)
            [^\s'"]+          # any non-whitespace, non-quote characters
            """,
            re.VERBOSE | re.IGNORECASE,
        )
        return pattern.findall(text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """
        从文本中提取目标路径。

        支持的关键字：
        - target path:
        - target_path:
        - path:
        - 目标路径:
        - 路径:
        """
        patterns = [
            r"target\s*path\s*:\s*([^\s'\"`]+)",
            r"target_path\s*:\s*([^\s'\"`]+)",
            r"path\s*:\s*([^\s'\"`]+)",
            r"目标路径\s*[:：]\s*([^\s'\"`]+)",
            r"路径\s*[:：]\s*([^\s'\"`]+)",
        ]
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                return m.group(1).strip()
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """
        从 GitHub URL 推断仓库名称。

        处理：
        - https://github.com/user/repo
        - https://github.com/user/repo.git
        - git@github.com:user/repo.git
        - git://github.com/user/repo.git
        """
        # Remove protocol and host
        url = re.sub(
            r"^(?:https?://|git@|git://)github\.com[:/]", "", url, flags=re.IGNORECASE)
        # Split path
        parts = url.split("/")
        if not parts:
            return ""
        repo = parts[-1]
        # Strip .git suffix if present
        repo = re.sub(r"\.git$", "", repo, flags=re.IGNORECASE)
        return repo
