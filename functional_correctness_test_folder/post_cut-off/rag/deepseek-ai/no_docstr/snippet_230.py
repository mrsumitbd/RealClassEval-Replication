
import os
from typing import Dict, List, Any
import requests
import json


class TavilySearchService:
    """Service for interacting with the Tavily Search API using the official SDK."""

    def __init__(self):
        """Initialize the Tavily search service with API key from environment."""
        self.api_key = os.getenv('TAVILY_API_KEY')
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY environment variable not set")
        self.base_url = "https://api.tavily.com"

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
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "max_results": max_results
        }
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains

        response = requests.post(f"{self.base_url}/search", json=payload)
        response.raise_for_status()
        return response.json()

    def extract(self, url: str) -> Dict[str, Any]:
        """
        Extract content from a specific URL using Tavily API.
        Args:
            url: The URL to extract content from
        Returns:
            Dict containing the extracted content
        """
        payload = {
            "api_key": self.api_key,
            "url": url
        }
        response = requests.post(f"{self.base_url}/extract", json=payload)
        response.raise_for_status()
        return response.json()

    def format_search_results(self, results: Dict[str, Any]) -> str:
        """Format search results into a readable string."""
        formatted = []
        for result in results.get('results', []):
            formatted.append(
                f"Title: {result.get('title', 'N/A')}\nURL: {result.get('url', 'N/A')}\nContent: {result.get('content', 'N/A')}\n")
        return "\n".join(formatted)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        """Format extract results into a readable string."""
        return f"Title: {results.get('title', 'N/A')}\nContent: {results.get('content', 'N/A')}\nURL: {results.get('url', 'N/A')}"
