
import re
from typing import List, Optional


class GitHubURLExtractor:

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        pattern = r'https?://github\.com/[^\s/$.?#].[^\s]*'
        urls = re.findall(pattern, text)
        return urls

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        pattern = r'https?://github\.com/[^\s/$.?#].[^\s]*#L(\d+)(?:-L(\d+))?'
        match = re.search(pattern, text)
        if match:
            start_line = match.group(1)
            end_line = match.group(2) if match.group(2) else start_line
            return f"L{start_line}-L{end_line}"
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        pattern = r'https?://github\.com/([^/]+/[^/]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return ""
