
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
        pattern = r'https?://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/(?:blob|tree)/[a-zA-Z0-9_.-]+/([a-zA-Z0-9_./-]+)'
        match = re.search(pattern, text)
        return match.group(1) if match else None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        pattern = r'https?://github\.com/([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)'
        match = re.search(pattern, url)
        return match.group(1) if match else ""
