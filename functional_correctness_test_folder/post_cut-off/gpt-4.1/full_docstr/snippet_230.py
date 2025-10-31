
import os
from typing import List, Dict, Any
from tavily import TavilyClient


class TavilySearchService:
    '''Service for interacting with the Tavily Search API using the official SDK.'''

    def __init__(self):
        '''Initialize the Tavily search service with API key from environment.'''
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable not set.")
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, search_depth: str = 'basic', topic: str = 'general', include_domains: List[str] | None = None, exclude_domains: List[str] | None = None, max_results: int = 5) -> Dict[str, Any]:
        '''
        Perform a web search using Tavily API.
        Args:
            query: The search query
            search_depth: 'basic' or 'advanced' search depth
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
            max_results: Maximum number of results to return
        Returns:
            Dict containing search results
        '''
        params = {
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "max_results": max_results
        }
        if include_domains is not None:
            params["include_domains"] = include_domains
        if exclude_domains is not None:
            params["exclude_domains"] = exclude_domains
        results = self.client.search(**params)
        return results

    def extract(self, url: str) -> Dict[str, Any]:
        '''
        Extract content from a specific URL using Tavily API.
        Args:
            url: The URL to extract content from
        Returns:
            Dict containing the extracted content
        '''
        results = self.client.extract(url=url)
        return results

    def format_search_results(self, results: Dict[str, Any]) -> str:
        '''Format search results into a readable string.'''
        if not results or "results" not in results:
            return "No results found."
        lines = []
        for idx, item in enumerate(results["results"], 1):
            title = item.get("title", "No Title")
            url = item.get("url", "No URL")
            snippet = item.get("snippet", "")
            lines.append(
                f"{idx}. {title}\n   URL: {url}\n   Snippet: {snippet}\n")
        return "\n".join(lines)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        '''Format extract results into a readable string.'''
        if not results:
            return "No content extracted."
        title = results.get("title", "No Title")
        url = results.get("url", "No URL")
        content = results.get("content", "")
        return f"Title: {title}\nURL: {url}\n\nContent:\n{content}"
