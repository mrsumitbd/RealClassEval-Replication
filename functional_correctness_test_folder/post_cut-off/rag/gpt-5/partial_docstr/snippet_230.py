import os
from typing import Any, Dict, List


class TavilySearchService:
    '''Service for interacting with the Tavily Search API using the official SDK.'''

    def __init__(self):
        '''Initialize the Tavily search service with API key from environment.'''
        api_key = os.getenv('TAVILY_API_KEY')
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable is not set.")
        try:
            from tavily import TavilyClient  # type: ignore
        except Exception as e:
            raise ImportError(
                "tavily package is required. Install with `pip install tavily-python`.") from e
        self._client = TavilyClient(api_key=api_key)

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
        if search_depth not in ('basic', 'advanced'):
            raise ValueError("search_depth must be 'basic' or 'advanced'")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer")
        return self._client.search(
            query=query,
            search_depth=search_depth,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            max_results=max_results,
            topic=topic,
        )

    def extract(self, url: str) -> Dict[str, Any]:
        '''
        Extract content from a specific URL using Tavily API.
        Args:
            url: The URL to extract content from
        Returns:
            Dict containing the extracted content
        '''
        if not url or not isinstance(url, str):
            raise ValueError("url must be a non-empty string")
        return self._client.extract(url=url)

    def format_search_results(self, results: Dict[str, Any]) -> str:
        '''Format search results into a readable string.'''
        if not results:
            return "No results."
        parts: List[str] = []
        query = results.get('query')
        if query:
            parts.append(f"Query: {query}")
        answer = results.get('answer')
        if answer:
            parts.append(f"Answer: {answer}")
        items = results.get('results') or []
        if not items:
            parts.append("No result items found.")
        else:
            for idx, item in enumerate(items, start=1):
                title = item.get('title') or 'Untitled'
                url = item.get('url') or 'No URL'
                content = item.get('content') or item.get(
                    'snippet') or item.get('text') or ''
                if content and len(content) > 400:
                    content = content[:400].rstrip() + "..."
                parts.append(f"{idx}. {title}\n   {url}\n   {content}")
        return "\n".join(parts)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        '''Format extract results into a readable string.'''
        if not results:
            return "No extracted content."
        title = results.get('title') or 'Untitled'
        url = results.get('url') or 'No URL'
        content = (
            results.get('content')
            or results.get('markdown')
            or results.get('raw_content')
            or results.get('text')
            or ''
        )
        preview = content
        if preview and len(preview) > 1000:
            preview = preview[:1000].rstrip() + "..."
        return f"Title: {title}\nURL: {url}\n\n{preview}"
