from typing import List, Dict, Any, Optional
import os

try:
    from tavily import TavilyClient
except Exception as e:
    TavilyClient = None


class TavilySearchService:
    '''Service for interacting with the Tavily Search API using the official SDK.'''

    def __init__(self):
        '''Initialize the Tavily search service with API key from environment.'''
        api_key = os.getenv("TAVILY_API_KEY") or os.getenv(
            "TAVILY_APIKEY") or os.getenv("TAVILY_API")
        if not api_key:
            raise RuntimeError(
                "TAVILY_API_KEY environment variable is not set.")
        if TavilyClient is None:
            raise RuntimeError(
                "tavily package is not installed. Please install with 'pip install tavily-python'.")
        self.client = TavilyClient(api_key=api_key)

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
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string.")
        if search_depth not in ('basic', 'advanced'):
            raise ValueError("search_depth must be 'basic' or 'advanced'.")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer.")
        include_domains = include_domains or []
        exclude_domains = exclude_domains or []
        if not isinstance(include_domains, list) or not all(isinstance(d, str) for d in include_domains):
            raise ValueError("include_domains must be a list of strings.")
        if not isinstance(exclude_domains, list) or not all(isinstance(d, str) for d in exclude_domains):
            raise ValueError("exclude_domains must be a list of strings.")

        return self.client.search(
            query=query,
            search_depth=search_depth,
            topic=topic,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            max_results=max_results,
        )

    def extract(self, url: str) -> Dict[str, Any]:
        '''
        Extract content from a specific URL using Tavily API.
        Args:
            url: The URL to extract content from
        Returns:
            Dict containing the extracted content
        '''
        if not isinstance(url, str) or not url.strip():
            raise ValueError("url must be a non-empty string.")
        return self.client.extract(url=url)

    def format_search_results(self, results: Dict[str, Any]) -> str:
        '''Format search results into a readable string.'''
        if not isinstance(results, dict):
            return "No results."
        lines: List[str] = []
        answer = results.get("answer")
        if answer:
            lines.append(f"Answer: {answer}")
        res_list = results.get("results") or results.get("data") or []
        if not isinstance(res_list, list):
            res_list = []
        if res_list:
            lines.append("Results:")
        for idx, item in enumerate(res_list, start=1):
            title = item.get("title") or item.get("name") or "Untitled"
            url = item.get("url") or item.get("link") or ""
            content = item.get("content") or item.get("snippet") or ""
            snippet = (content[:300] + "…") if isinstance(content,
                                                          str) and len(content) > 300 else content
            lines.append(f"{idx}. {title}")
            if url:
                lines.append(f"   URL: {url}")
            if snippet:
                lines.append(f"   Snippet: {snippet}")
        if not lines:
            return "No results."
        return "\n".join(lines)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        '''Format extract results into a readable string.'''
        if not isinstance(results, dict):
            return "No extracted content."
        title = results.get("title") or "Untitled"
        url = results.get("url") or ""
        content = results.get("content") or ""
        snippet = (content[:2000] + "…") if isinstance(content,
                                                       str) and len(content) > 2000 else content
        lines = [f"Title: {title}"]
        if url:
            lines.append(f"URL: {url}")
        if snippet:
            lines.append("Content:")
            lines.append(snippet)
        else:
            lines.append("No content found.")
        return "\n".join(lines)
