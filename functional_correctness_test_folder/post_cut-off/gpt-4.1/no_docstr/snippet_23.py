
import re
from typing import List, Optional


class GitHubURLExtractor:

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        pattern = r'https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[^\s"\'\)\]]*)?'
        return re.findall(pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        # Look for patterns like "path: <path>" or "target path: <path>"
        match = re.search(
            r'(?:path|target path)\s*:\s*([^\s,;]+)', text, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        # Extract the owner/repo from the URL
        match = re.match(
            r'https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)', url)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
        return ""
