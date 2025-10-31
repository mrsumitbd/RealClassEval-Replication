
import os
from tavily import TavilyClient
from typing import Any, Dict, List, Optional


class TavilySearchService:
    """Service for interacting with the Tavily Search API using the official SDK."""

    def __init__(self):
        """Initialize the Tavily search service with API key from environment."""
        api_key = os.getenv('TAVILY_API_KEY')
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable is not set")
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, search_depth: str = 'basic', topic: str = 'general', include_domains: Optional[List[str]] = None, exclude_domains: Optional[List[str]] = None, max_results: int = 5) -> Dict[str, Any]:
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
        response = self.client.search(query=query, search_depth=search_depth, topic=topic,
                                      include_domains=include_domains, exclude_domains=exclude_domains, max_results=max_results)
        return response

    def extract(self, url: str) -> Dict[str, Any]:
        """
        Extract content from a specific URL using Tavily API.

        Args:
            url: The URL to extract content from

        Returns:
            Dict containing the extracted content
        """
        response = self.client.get(url=url)
        return response

    def format_search_results(self, results: Dict[str, Any]) -> str:
        """Format search results into a readable string."""
        formatted_results = ""
        for result in results.get('results', []):
            formatted_results += f"Title: {result.get('title')}\n"
            formatted_results += f"URL: {result.get('url')}\n"
            formatted_results += f"Content: {result.get('content')}\n\n"
        return formatted_results

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        """Format extract results into a readable string."""
        return results.get('content', '')
