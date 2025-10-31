
import os
from typing import List, Dict, Any
from tavily_search_sdk import TavilyClient


class TavilySearchService:
    '''Service for interacting with the Tavily Search API using the official SDK.'''

    def __init__(self):
        '''Initialize the Tavily search service with API key from environment.'''
        api_key = os.getenv('TAVILY_API_KEY')
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable not set")
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, search_depth: str = 'basic', topic: str = 'general', include_domains: List[str] | None = None, exclude_domains: List[str] | None = None, max_results: int = 5) -> Dict[str, Any]:
        '''
        Perform a web search using Tavily API.
        Args:
            query: The search query
            search_depth: 'basic' or 'advanced' search depth
            topic: The topic of the search
            include_domains: List of domains to include in search
            exclude_domains: List of domains to exclude from search
            max_results: Maximum number of results to return
        Returns:
            Dict containing search results
        '''
        return self.client.search(
            query=query,
            search_depth=search_depth,
            topic=topic,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            max_results=max_results
        )

    def extract(self, url: str) -> Dict[str, Any]:
        '''Extract information from a given URL using Tavily API.'''
        return self.client.extract(url=url)

    def format_search_results(self, results: Dict[str, Any]) -> str:
        '''Format search results into a readable string.'''
        formatted_results = []
        for result in results.get('results', []):
            title = result.get('title', 'No title')
            link = result.get('link', 'No link')
            snippet = result.get('snippet', 'No snippet')
            formatted_results.append(
                f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
        return "\n".join(formatted_results)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        '''Format extract results into a readable string.'''
        title = results.get('title', 'No title')
        content = results.get('content', 'No content')
        return f"Title: {title}\nContent: {content}"
