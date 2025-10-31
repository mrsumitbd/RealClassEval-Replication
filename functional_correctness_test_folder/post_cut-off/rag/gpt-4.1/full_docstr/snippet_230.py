import os
from typing import Any, Dict, List, Optional
import tavily


class TavilySearchService:
    '''Service for interacting with the Tavily Search API using the official SDK.'''

    def __init__(self):
        '''Initialize the Tavily search service with API key from environment.'''
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable not set")
        self.client = tavily.Client(api_key=api_key)

    def search(
        self,
        query: str,
        search_depth: str = 'basic',
        topic: str = 'general',
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        max_results: int = 5
    ) -> Dict[str, Any]:
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
        return self.client.search(**params)

    def extract(self, url: str) -> Dict[str, Any]:
        '''
        Extract content from a specific URL using Tavily API.
        Args:
            url: The URL to extract content from
        Returns:
            Dict containing the extracted content
        '''
        return self.client.extract(url=url)

    def format_search_results(self, results: Dict[str, Any]) -> str:
        '''Format search results into a readable string.'''
        items = results.get("results") or results.get("data") or []
        if not items:
            return "No search results found."
        lines = []
        for idx, item in enumerate(items, 1):
            title = item.get("title", "")
            url = item.get("url", "")
            snippet = item.get("content", "") or item.get("snippet", "")
            lines.append(f"{idx}. {title}\nURL: {url}\nSnippet: {snippet}\n")
        return "\n".join(lines)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        '''Format extract results into a readable string.'''
        title = results.get("title", "")
        url = results.get("url", "")
        content = results.get("content", "")
        if not content:
            return "No content extracted."
        return f"Title: {title}\nURL: {url}\n\nContent:\n{content}"
