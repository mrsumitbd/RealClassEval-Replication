
import requests
from typing import List, Dict, Any


class TavilySearchService:

    def __init__(self):
        self.base_url = "https://api.tavily.com"
        self.headers = {
            "Content-Type": "application/json",
        }

    def search(self, query: str, search_depth: str = 'basic', topic: str = 'general', include_domains: List[str] | None = None, exclude_domains: List[str] | None = None, max_results: int = 5) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/search"
        payload = {
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "include_domains": include_domains,
            "exclude_domains": exclude_domains,
            "max_results": max_results
        }
        response = requests.post(endpoint, json=payload, headers=self.headers)
        return response.json()

    def extract(self, url: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/extract"
        payload = {
            "url": url
        }
        response = requests.post(endpoint, json=payload, headers=self.headers)
        return response.json()

    def format_search_results(self, results: Dict[str, Any]) -> str:
        formatted_results = ""
        for result in results.get('results', []):
            formatted_results += f"Title: {result.get('title', 'N/A')}\n"
            formatted_results += f"URL: {result.get('url', 'N/A')}\n"
            formatted_results += f"Content: {result.get('content', 'N/A')}\n\n"
        return formatted_results

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        formatted_results = ""
        formatted_results += f"Title: {results.get('title', 'N/A')}\n"
        formatted_results += f"URL: {results.get('url', 'N/A')}\n"
        formatted_results += f"Content: {results.get('content', 'N/A')}\n"
        return formatted_results
