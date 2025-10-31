from typing import List, Dict, Any, Optional
import os

try:
    from tavily import TavilyClient
except Exception:  # pragma: no cover
    TavilyClient = None


class TavilySearchService:
    '''Service for interacting with the Tavily Search API using the official SDK.'''

    def __init__(self):
        '''Initialize the Tavily search service with API key from environment.'''
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "TAVILY_API_KEY environment variable is not set.")
        if TavilyClient is None:
            raise ImportError(
                "tavily package is not installed. Install with `pip install tavily-python`.")
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
        if search_depth not in ("basic", "advanced"):
            raise ValueError("search_depth must be 'basic' or 'advanced'.")
        if not isinstance(max_results, int) or max_results <= 0:
            raise ValueError("max_results must be a positive integer.")
        try:
            return self.client.search(
                query=query.strip(),
                search_depth=search_depth,
                topic=topic,
                include_domains=include_domains,
                exclude_domains=exclude_domains,
                max_results=max_results,
            )
        except Exception as e:
            return {"error": str(e)}

    def extract(self, url: str) -> Dict[str, Any]:
        if not isinstance(url, str) or not url.strip():
            raise ValueError("url must be a non-empty string.")
        try:
            return self.client.extract(url=url.strip())
        except Exception as e:
            return {"error": str(e)}

    def format_search_results(self, results: Dict[str, Any]) -> str:
        if not isinstance(results, dict):
            return "No results."
        if "error" in results:
            return f"Error: {results.get('error')}"
        lines: List[str] = []
        answer = results.get("answer")
        if answer:
            lines.append(f"Answer: {answer}")
        items = results.get("results") or results.get("data") or []
        if not isinstance(items, list) or not items:
            if lines:
                return "\n".join(lines)
            return "No search results."
        for idx, item in enumerate(items, start=1):
            title = (item.get("title") or "").strip() or "Untitled"
            url = (item.get("url") or "").strip()
            content = (item.get("content") or item.get(
                "snippet") or "").strip()
            snippet = content[:300] + ("..." if len(content) > 300 else "")
            parts = [f"{idx}. {title}"]
            if url:
                parts.append(f"   {url}")
            if snippet:
                parts.append(f"   {snippet}")
            lines.append("\n".join(parts))
        return "\n".join(lines)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        '''Format extract results into a readable string.'''
        if not isinstance(results, dict):
            return "No extract results."
        if "error" in results:
            return f"Error: {results.get('error')}"
        title = (results.get("title") or "").strip()
        url = (results.get("url") or "").strip()
        content = (results.get("content") or results.get("text") or "").strip()
        if not (title or url or content):
            return "No extractable content."
        lines: List[str] = []
        if title:
            lines.append(title)
        if url:
            lines.append(url)
        if content:
            preview = content[:2000] + ("..." if len(content) > 2000 else "")
            lines.append(preview)
        return "\n".join(lines)
