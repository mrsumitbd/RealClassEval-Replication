
import re
from typing import List, Optional


class GitHubURLExtractor:

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        pattern = r'https?://(?:www\.)?github\.com/[^\s]+'
        return re.findall(pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        pattern = r'https?://(?:www\.)?github\.com/[^\s]+/(?:tree|blob)/[^\s]+'
        match = re.search(pattern, text)
        if match:
            url = match.group()
            path = url.split('/')[-1]
            return path
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        pattern = r'https?://(?:www\.)?github\.com/([^/]+)/([^/]+)'
        match = re.match(pattern, url)
        if match:
            return match.group(2)
        return ''
