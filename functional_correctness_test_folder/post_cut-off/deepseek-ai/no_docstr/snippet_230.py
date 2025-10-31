
from typing import List, Dict, Any
import requests
import json


class TavilySearchService:

    def __init__(self):
        self.base_url = "https://api.tavily.com"
        self.api_key = None  # Set your API key here or via environment variable

    def search(self, query: str, search_depth: str = 'basic', topic: str = 'general', include_domains: List[str] | None = None, exclude_domains: List[str] | None = None, max_results: int = 5) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/search"
        payload = {
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "include_domains": include_domains if include_domains else [],
            "exclude_domains": exclude_domains if exclude_domains else [],
            "max_results": max_results
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()

    def extract(self, url: str) -> Dict[str, Any]:
        endpoint = f"{self.base_url}/extract"
        payload = {
            "url": url
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()

    def format_search_results(self, results: Dict[str, Any]) -> str:
        formatted_results = []
        if 'results' in results:
            for result in results['results']:
                formatted_result = f"Title: {result.get('title', 'N/A')}\nURL: {result.get('url', 'N/A')}\nContent: {result.get('content', 'N/A')}\n"
                formatted_results.append(formatted_result)
        return "\n".join(formatted_results)

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        formatted_result = f"Title: {results.get('title', 'N/A')}\nURL: {results.get('url', 'N/A')}\nContent: {results.get('content', 'N/A')}\n"
        return formatted_result
