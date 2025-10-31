import os
from typing import Any, Dict, List


class TavilySearchService:
    '''Service for interacting with the Tavily Search API using the official SDK.'''

    def __init__(self):
        '''Initialize the Tavily search service with API key from environment.'''
        api_key = os.getenv('TAVILY_API_KEY')
        if not api_key:
            raise ValueError('TAVILY_API_KEY environment variable is not set.')
        try:
            from tavily import TavilyClient
        except ImportError as e:
            raise ImportError(
                'tavily package is not installed. Install with: pip install tavily-python') from e
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
        if not isinstance(query, str) or not query.strip():
            raise ValueError('query must be a non-empty string.')
        if search_depth not in {'basic', 'advanced'}:
            raise ValueError("search_depth must be 'basic' or 'advanced'.")
        if max_results <= 0:
            raise ValueError('max_results must be a positive integer.')

        kwargs: Dict[str, Any] = {
            'search_depth': search_depth,
            'max_results': max_results,
            'topic': topic,
        }
        if include_domains:
            kwargs['include_domains'] = include_domains
        if exclude_domains:
            kwargs['exclude_domains'] = exclude_domains

        return self._client.search(query=query, **kwargs)

    def extract(self, url: str) -> Dict[str, Any]:
        '''
        Extract content from a specific URL using Tavily API.
        Args:
            url: The URL to extract content from
        Returns:
            Dict containing the extracted content
        '''
        if not isinstance(url, str) or not url.strip():
            raise ValueError('url must be a non-empty string.')
        return self._client.extract(url=url)

    def format_search_results(self, results: Dict[str, Any]) -> str:
        '''Format search results into a readable string.'''
        if not results:
            return 'No results.'
        lines: List[str] = []
        if (query := results.get('query')):
            lines.append(f'Query: {query}')
        if (answer := results.get('answer')):
            lines.append(f'Answer: {answer}')
        items = results.get('results') or []
        if not items:
            if not lines:
                return 'No results.'
            return '\n'.join(lines)
        lines.append('Results:')
        for idx, item in enumerate(items, start=1):
            title = item.get('title') or 'Untitled'
            url = item.get('url') or ''
            snippet = item.get('snippet') or item.get('content') or ''
            snippet = snippet.strip().replace('\n', ' ')
            if len(snippet) > 300:
                snippet = snippet[:300].rstrip() + '...'
            lines.append(f'{idx}. {title}')
            if url:
                lines.append(f'   URL: {url}')
            if snippet:
                lines.append(f'   Snippet: {snippet}')
        return '\n'.join(lines)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        '''Format extract results into a readable string.'''
        if not results:
            return 'No extracted content.'
        title = results.get('title') or 'Untitled'
        url = results.get('url') or results.get('source_url') or ''
        content = results.get('content') or results.get(
            'raw_content') or results.get('text') or ''
        content = (content or '').strip()
        if len(content) > 1000:
            content = content[:1000].rstrip() + '...'
        lines = [f'Title: {title}']
        if url:
            lines.append(f'URL: {url}')
        if content:
            lines.append('Content:')
            lines.append(content)
        else:
            lines.append('No content extracted.')
        return '\n'.join(lines)
