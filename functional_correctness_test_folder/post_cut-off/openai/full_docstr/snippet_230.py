
import os
from typing import List, Dict, Any

try:
    from tavily import TavilyClient
except ImportError as exc:
    raise ImportError(
        "The tavily SDK is required for TavilySearchService. "
        "Install it with `pip install tavily`."
    ) from exc


class TavilySearchService:
    """Service for interacting with the Tavily Search API using the official SDK."""

    def __init__(self):
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
        include_domains: List[str] | None = None,
        exclude_domains: List[str] | None = None,
        max_results: int = 5,
    ) -> Dict[str, Any]:
        """
        Perform a web search using Tavily API.

        Args:
            query: The search query
            search_depth: 'basic' or 'advanced' search depth
            topic: Search topic (unused by the SDK but kept for compatibility)
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
            max_results: Maximum number of results to return

        Returns:
            Dict containing search results
        """
        # The SDK does not expose a `topic` parameter, but we keep it for API compatibility.
        params: Dict[str, Any] = {
            "query": query,
            "search_depth": search_depth,
            "include_domains": include_domains,
            "exclude_domains": exclude_domains,
            "max_results": max_results,
        }
        # Remove None values to avoid sending them to the API
        params = {k: v for k, v in params.items() if v is not None}
        return self.client.search(**params)

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
        output_lines: List[str] = []
        items = results.get("results", [])
        if not items:
            return "No results found."

        for idx, item in enumerate(items, start=1):
            title = item.get("title", "No title")
            url = item.get("url", "No URL")
            description = item.get("description", "No description")
            output_lines.append(
                f"{idx}. {title}\n   {url}\n   {description}\n")

        return "\n".join(output_lines)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        """Format extract results into a readable string."""
        output_lines: List[str] = []
        title = results.get("title", "No title")
        url = results.get("url", "No URL")
        content = results.get("content", "No content")
        summary = results.get("summary")

        output_lines.append(f"Title: {title}")
        output_lines.append(f"URL: {url}")
        if summary:
            output_lines.append(f"Summary: {summary}")
        output_lines.append("\nContent:\n")
        output_lines.append(content)

        return "\n".join(output_lines)
