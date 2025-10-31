
import os
import json
import requests
from typing import List, Dict, Any, Optional


class TavilySearchService:
    """
    A simple wrapper around the Tavily API for searching and extracting web content.
    """

    BASE_URL = "https://api.tavily.com"

    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY environment variable is required")

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers,
                                 json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def search(
        self,
        query: str,
        search_depth: str = "basic",
        topic: str = "general",
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        max_results: int = 5,
    ) -> Dict[str, Any]:
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "max_results": max_results,
        }
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains
        return self._post("/search", payload)

    def extract(self, url: str) -> Dict[str, Any]:
        payload = {"api_key": self.api_key, "url": url}
        return self._post("/extract", payload)

    def format_search_results(self, results: Dict[str, Any]) -> str:
        if not results or "results" not in results:
            return "No results found."
        lines = []
        for i, item in enumerate(results["results"], start=1):
            title = item.get("title", "No title")
            url = item.get("url", "")
            snippet = item.get("snippet", "")
            lines.append(
                f"{i}. {title}\n   URL: {url}\n   Snippet: {snippet}\n")
        return "\n".join(lines)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        if not results or "content" not in results:
            return "No content extracted."
        title = results.get("title", "Untitled")
        url = results.get("url", "")
        content = results.get("content", "")
        return f"Title: {title}\nURL: {url}\n\n{content}"
