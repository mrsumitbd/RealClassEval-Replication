
import os
from typing import List, Dict, Any, Optional

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
                "TAVILY_API_KEY environment variable is not set. "
                "Please set it to your Tavily API key."
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
            query: The search query.
            search_depth: 'basic' or 'advanced' search depth.
            topic: Search topic (unused by the SDK but kept for compatibility).
            include_domains: List of domains to include in search.
            exclude_domains: List of domains to exclude from search.
            max_results: Maximum number of results to return.

        Returns:
            Dict containing search results.
        """
        # The Tavily SDK does not expose a `topic` parameter; it is kept for API compatibility.
        params: Dict[str, Any] = {
            "query": query,
            "search_depth": search_depth,
            "max_results": max_results,
        }
        if include_domains:
            params["include_domains"] = include_domains
        if exclude_domains:
            params["exclude_domains"] = exclude_domains

        try:
            results = self.client.search(**params)
        except Exception as exc:
            raise RuntimeError(f"Search failed: {exc}") from exc

        return results

    def extract(self, url: str) -> Dict[str, Any]:
        """
        Extract content from a URL using Tavily API.

        Args:
            url: The URL to extract content from.

        Returns:
            Dict containing extracted content.
        """
        try:
            result = self.client.extract(url)
        except Exception as exc:
            raise RuntimeError(f"Extraction failed for {url}: {exc}") from exc
        return result

    def format_search_results(self, results: Dict[str, Any]) -> str:
        """
        Format search results into a readable string.

        Args:
            results: The raw results dictionary from Tavily.

        Returns:
            A formatted string representation of the search results.
        """
        if not results or "results" not in results:
            return "No results found."

        lines = []
        for idx, item in enumerate(results["results"], start=1):
            title = item.get("title", "No title")
            url = item.get("url", "No URL")
            snippet = item.get("snippet", "")
            lines.append(f"{idx}. {title}\n   {url}\n   {snippet}\n")

        return "\n".join(lines)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        """
        Format extract results into a readable string.

        Args:
            results: The raw extract dictionary from Tavily.

        Returns:
            A formatted string representation of the extracted content.
        """
        if not results:
            return "No extract data available."

        title = results.get("title", "No title")
        url = results.get("url", "No URL")
        content = results.get("content", "No content")

        return f"Title: {title}\nURL: {url}\n\n{content}"
