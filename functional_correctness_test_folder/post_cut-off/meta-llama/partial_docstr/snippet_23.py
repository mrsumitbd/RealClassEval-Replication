
import re
from typing import List, Optional


class GitHubURLExtractor:

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        pattern = r"https?://(?:www\.)?github\.com/[^\s]+"
        return re.findall(pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        pattern = r"target path[:\s]+([^\s]+)"
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        pattern = r"github\.com/([^/]+/[^/]+)"
        match = re.search(pattern, url)
        return match.group(1).strip() if match else ""
