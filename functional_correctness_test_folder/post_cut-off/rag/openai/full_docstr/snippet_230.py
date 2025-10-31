
import os
from typing import Any, Dict, List, Optional

# The official Tavily SDK
try:
    from tavily import TavilyClient
except ImportError as exc:
    raise ImportError(
        "The Tavily SDK is required for TavilySearchService. "
        "Install it with `pip install tavily`."
    ) from exc


class TavilySearchService:
    """Service for interacting with the Tavily Search API using the official SDK."""

    def __init__(self) -> None:
        """Initialize the Tavily search service with API key from environment."""
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY environment variable is required to use TavilySearchService."
            )
        self.client = TavilyClient(api_key=api_key)

    def search(
        self,
        query: str,
        search_depth: str = "basic",
        topic: str = "general",
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        max_results: int = 5,
    ) -> Dict[str, Any]:
        """
        Perform a web search using Tavily API.

        Args:
            query: The search query
            search_depth: 'basic' or 'advanced' search depth
            topic: The topic to focus the search on
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
            max_results: Maximum number of results to return

        Returns:
            Dict containing search results
        """
        # Build the request payload
        payload: Dict[str, Any] = {
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "max_results": max_results,
        }
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains

        # Execute the search
        return self.client.search(**payload)

    def extract(self, url: str) -> Dict[str, Any]:
        """
        Extract content from a specific URL using Tavily API.

        Args:
            url: The URL to extract content from

        Returns:
            Dict containing the extracted content
        """
        return self.client.extract(url=url)

    def format_search_results(self, results: Dict[str, Any]) -> str:
        """Format search results into a readable string."""
        # Tavily returns a dict with a 'results' key containing a list of result dicts
        items = results.get("results", [])
        if not items:
            return "No results found."

        lines: List[str] = []
        for idx, item in enumerate(items, start=1):
            title = item.get("title", "No title")
            url = item.get("url", "No URL")
            snippet = item.get("content", "")[:200]  # truncate for brevity
            lines.append(
                f"{idx}. {title}\n   URL: {url}\n   Snippet: {snippet}\n")

        return "\n".join(lines)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        """Format extract results into a readable string."""
        # Tavily extract returns a dict with a 'content' key
        content = results.get("content")
        if not content:
            return "No content extracted."

        # If the content is a list of paragraphs, join them
        if isinstance(content, list):
            return "\n\n".join(content)
        return str(content)
