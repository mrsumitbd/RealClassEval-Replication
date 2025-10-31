
import re
from typing import List, Optional


class GitHubURLExtractor:

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        github_url_pattern = r'https?://(?:www\.)?github\.com/[^\s]+'
        return re.findall(github_url_pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        path_pattern = r'https?://(?:www\.)?github\.com/[^\s]+/(?:tree|blob)/[^\s]+'
        match = re.search(path_pattern, text)
        if match:
            url = match.group()
            return url.split('/')[-1]
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        repo_name_pattern = r'https?://(?:www\.)?github\.com/([^/]+)/([^/]+)'
        match = re.match(repo_name_pattern, url)
        if match:
            return match.group(2)
        return ''
