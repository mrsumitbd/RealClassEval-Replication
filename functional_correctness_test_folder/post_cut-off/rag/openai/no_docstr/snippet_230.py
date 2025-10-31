
import os
from typing import Any, Dict, List, Optional

from tavily import TavilyClient


class TavilySearchService:
    '''Service for interacting with the Tavily Search API using the official SDK.'''

    def __init__(self):
        '''Initialize the Tavily search service with API key from environment.'''
        api_key = os.getenv('TAVILY_API_KEY')
        if not api_key:
            raise ValueError('TAVILY_API_KEY environment variable is required')
        self.client = TavilyClient(api_key=api_key)

    def search(
        self,
        query: str,
        search_depth: str = 'basic',
        topic: str = 'general',
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        max_results: int = 5,
    ) -> Dict[str, Any]:
        '''
        Perform a web search using Tavily API.
        Args:
            query: The search query
            search_depth: 'basic' or 'advanced' search depth
            topic: Search topic (unused by SDK but kept for compatibility)
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
            max_results: Maximum number of results to return
        Returns:
            Dict containing search results
        '''
        params: Dict[str, Any] = {
            'query': query,
            'search_depth': search_depth,
            'max_results': max_results,
        }
        if include_domains:
            params['include_domains'] = include_domains
        if exclude_domains:
            params['exclude_domains'] = exclude_domains
        # The SDK does not expose a 'topic' parameter; ignore if present
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
        output_lines: List[str] = []
        items = results.get('results', [])
        for idx, item in enumerate(items, start=1):
            title = item.get('title', 'No title')
            url = item.get('url', 'No URL')
            snippet = item.get('content', '')[:200]
            output_lines.append(f"{idx}. {title}\n   {url}\n   {snippet}\n")
        return "\n".join(output_lines)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        '''Format extract results into a readable string.'''
        title = results.get('title', 'No title')
        url = results.get('url', 'No URL')
        content = results.get('content', '')
        return f"Title: {title}\nURL: {url}\n\n{content}"
