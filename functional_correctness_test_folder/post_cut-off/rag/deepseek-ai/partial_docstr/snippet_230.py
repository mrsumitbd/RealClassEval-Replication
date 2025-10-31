
import os
from typing import Dict, List, Any
from tavily import TavilyClient


class TavilySearchService:
    """Service for interacting with the Tavily Search API using the official SDK."""

    def __init__(self):
        """Initialize the Tavily search service with API key from environment."""
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def search(self, query: str, search_depth: str = 'basic', topic: str = 'general', include_domains: List[str] | None = None, exclude_domains: List[str] | None = None, max_results: int = 5) -> Dict[str, Any]:
        """
        Perform a web search using Tavily API.
        Args:
            query: The search query
            search_depth: 'basic' or 'advanced' search depth
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
            max_results: Maximum number of results to return
        Returns:
            Dict containing search results
        """
        return self.client.search(
            query=query,
            search_depth=search_depth,
            topic=topic,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            max_results=max_results
        )

    def extract(self, url: str) -> Dict[str, Any]:
        """
        Extract content from a specific URL using Tavily API.
        Args:
            url: The URL to extract content from
        Returns:
            Dict containing the extracted content
        """
        return self.client.extract(url)

    def format_search_results(self, results: Dict[str, Any]) -> str:
        """Format search results into a readable string."""
        formatted = []
        for result in results.get("results", []):
            formatted.append(
                f"Title: {result.get('title', 'N/A')}\nURL: {result.get('url', 'N/A')}\nContent: {result.get('content', 'N/A')}\n")
        return "\n".join(formatted)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        """Format extract results into a readable string."""
        return f"Title: {results.get('title', 'N/A')}\nURL: {results.get('url', 'N/A')}\nContent: {results.get('content', 'N/A')}\n"
