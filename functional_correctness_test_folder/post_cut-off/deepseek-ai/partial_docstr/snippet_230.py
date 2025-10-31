
from typing import List, Dict, Any
import os
from tavily import TavilyClient


class TavilySearchService:
    '''Service for interacting with the Tavily Search API using the official SDK.'''

    def __init__(self):
        '''Initialize the Tavily search service with API key from environment.'''
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

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
        search_params = {
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "include_domains": include_domains,
            "exclude_domains": exclude_domains,
            "max_results": max_results
        }
        return self.client.search(**search_params)

    def extract(self, url: str) -> Dict[str, Any]:
        '''Extract content from a URL using Tavily API.'''
        return self.client.extract_content(url)

    def format_search_results(self, results: Dict[str, Any]) -> str:
        '''Format search results into a readable string.'''
        formatted_results = []
        if "results" in results:
            for result in results["results"]:
                formatted_results.append(
                    f"Title: {result.get('title', 'N/A')}\n"
                    f"URL: {result.get('url', 'N/A')}\n"
                    f"Content: {result.get('content', 'N/A')}\n"
                )
        return "\n".join(formatted_results) if formatted_results else "No results found."

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        '''Format extract results into a readable string.'''
        formatted_result = (
            f"Title: {results.get('title', 'N/A')}\n"
            f"URL: {results.get('url', 'N/A')}\n"
            f"Content: {results.get('content', 'N/A')}\n"
            f"Extracted Content: {results.get('extracted_content', 'N/A')}\n"
        )
        return formatted_result
