import os
from typing import Any, Dict, List


class TavilySearchService:
    '''Service for interacting with the Tavily Search API using the official SDK.'''

    def __init__(self):
        '''Initialize the Tavily search service with API key from environment.'''
        try:
            from tavily import TavilyClient  # type: ignore
        except Exception as e:
            raise ImportError(
                "The 'tavily' package is required. Install it with: pip install tavily-python") from e
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable not set.")
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
            raise ValueError("query must be a non-empty string.")
        if search_depth not in {"basic", "advanced"}:
            raise ValueError(
                "search_depth must be either 'basic' or 'advanced'.")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer.")
        return self._client.search(
            query=query.strip(),
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
        if not isinstance(url, str) or not url.strip():
            raise ValueError("url must be a non-empty string.")
        return self._client.extract(url=url.strip())

    def format_search_results(self, results: Dict[str, Any]) -> str:
        '''Format search results into a readable string.'''
        lines: List[str] = []
        query = results.get("query")
        if query:
            lines.append(f"Query: {query}")
        answer = results.get("answer")
        if answer:
            lines.append(f"Answer: {answer}")
        items = results.get("results") or []
        if items:
            lines.append("Results:")
            for idx, item in enumerate(items, start=1):
                title = item.get("title") or item.get("url") or "Untitled"
                url = item.get("url") or ""
                content = item.get("content") or item.get("snippet") or ""
                score = item.get("score")
                published = item.get(
                    "published_date") or item.get("date") or ""
                snippet = content.strip().replace("\n", " ")
                if len(snippet) > 300:
                    snippet = snippet[:300].rstrip() + "..."
                line = f"- {idx}. {title}"
                if url:
                    line += f" ({url})"
                if published:
                    line += f" | Published: {published}"
                if score is not None:
                    line += f" | Score: {score}"
                lines.append(line)
                if snippet:
                    lines.append(f"  Summary: {snippet}")
        else:
            lines.append("No results found.")
        return "\n".join(lines)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        '''Format extract results into a readable string.'''
        title = results.get("title") or "Untitled"
        url = results.get("url") or ""
        content = results.get("content") or results.get(
            "raw_content") or results.get("text") or ""
        content = content.strip()
        if len(content) > 1200:
            content = content[:1200].rstrip() + "..."
        lines = [f"Title: {title}"]
        if url:
            lines.append(f"URL: {url}")
        if content:
            lines.append("Content:")
            lines.append(content)
        else:
            lines.append("No content extracted.")
        return "\n".join(lines)
