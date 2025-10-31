
import re
from typing import List, Optional
from urllib.parse import urlparse, unquote


class GitHubURLExtractor:
    """
    Utility class for extracting GitHub URLs and related information from text.
    """

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """
        Extract all GitHub URLs from the given text.

        Parameters
        ----------
        text : str
            The input text to search for GitHub URLs.

        Returns
        -------
        List[str]
            A list of GitHub URLs found in the text.
        """
        # Matches http(s)://github.com/... with optional .git suffix and any trailing path
        pattern = re.compile(
            r"https?://github\.com/[^\s)]+",
            re.IGNORECASE,
        )
        return pattern.findall(text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """
        Extract the target path that follows the repository name in the first GitHub URL
        found in the text.

        For example, given the URL
            https://github.com/owner/repo/tree/main/src
        this method will return "tree/main/src".

        Parameters
        ----------
        text : str
            The input text containing a GitHub URL.

        Returns
        -------
        Optional[str]
            The target path after the repository name, or None if not found.
        """
        urls = GitHubURLExtractor.extract_github_urls(text)
        if not urls:
            return None

        url = urls[0]
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split("/") if p]
        if len(path_parts) < 2:
            return None

        # The first two parts are owner and repo
        target_parts = path_parts[2:]  # everything after the repo
        if not target_parts:
            return None

        return "/".join(target_parts)

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """
        Infer the repository name from a GitHub URL.

        Parameters
        ----------
        url : str
            A GitHub URL.

        Returns
        -------
        str
            The repository name (without the optional .git suffix).
        """
        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split("/") if p]
        if not path_parts:
            raise ValueError(f"Cannot infer repository name from URL: {url}")

        repo = path_parts[1] if len(path_parts) >= 2 else path_parts[0]
        # Strip optional .git suffix
        if repo.endswith(".git"):
            repo = repo[:-4]
        return unquote(repo)
