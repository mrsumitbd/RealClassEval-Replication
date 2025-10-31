
import re
from typing import List, Optional


class GitHubURLExtractor:

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        pattern = r'https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[^\s"\'<>]*)?'
        return re.findall(pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        # 目标路径格式假定为: target path: <path> 或 target: <path> 或 目标路径：<path>
        patterns = [
            r'target\s*path\s*[:：]\s*([^\s\n\r]+)',
            r'target\s*[:：]\s*([^\s\n\r]+)',
            r'目标路径\s*[:：]\s*([^\s\n\r]+)'
        ]
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                return m.group(1)
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        # Remove trailing slashes and query/fragment
        url = re.sub(r'[#?].*$', '', url.rstrip('/'))
        m = re.match(
            r'https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)', url)
        if m:
            return f"{m.group(1)}/{m.group(2)}"
        return ""
