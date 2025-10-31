
from typing import List, Optional
import re
from urllib.parse import urlparse


class GitHubURLExtractor:

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        pattern = r"https?://(?:www\.)?github\.com/[^\s]+"
        return re.findall(pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        github_urls = GitHubURLExtractor.extract_github_urls(text)
        if not github_urls:
            return None
        return github_urls[0]

    @staticmethod
    def infer_repo_name(url: str) -> str:
        parsed_url = urlparse(url)
        path_components = parsed_url.path.strip('/').split('/')
        if len(path_components) < 2:
            return ''
        return f"{path_components[-2]}/{path_components[-1]}"
