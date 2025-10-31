
import re
from typing import List, Optional


class GitHubURLExtractor:

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        pattern = r'https?://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+'
        urls = re.findall(pattern, text)
        return urls

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        pattern = r'https?://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+(/[a-zA-Z0-9_.\-/]+)?'
        match = re.search(pattern, text)
        if match:
            path = match.group(1)
            return path if path else None
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        pattern = r'https?://github\.com/([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return ""
