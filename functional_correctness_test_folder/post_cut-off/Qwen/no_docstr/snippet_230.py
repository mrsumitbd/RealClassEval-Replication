
from typing import List, Dict, Any


class TavilySearchService:

    def __init__(self):
        self.base_url = "https://api.tavily.com/search"
        self.api_key = "YOUR_API_KEY"  # Replace with your actual API key

    def search(self, query: str, search_depth: str = 'basic', topic: str = 'general', include_domains: List[str] | None = None, exclude_domains: List[str] | None = None, max_results: int = 5) -> Dict[str, Any]:
        import requests
        params = {
            'query': query,
            'search_depth': search_depth,
            'topic': topic,
            'include_domains': ','.join(include_domains) if include_domains else None,
            'exclude_domains': ','.join(exclude_domains) if exclude_domains else None,
            'max_results': max_results,
            'api_key': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

    def extract(self, url: str) -> Dict[str, Any]:
        import requests
        params = {
            'url': url,
            'api_key': self.api_key
        }
        response = requests.get(f"{self.base_url}/extract", params=params)
        return response.json()

    def format_search_results(self, results: Dict[str, Any]) -> str:
        formatted_results = ""
        for i, result in enumerate(results.get('results', []), start=1):
            formatted_results += f"Result {i}:\n"
            formatted_results += f"Title: {result.get('title', 'N/A')}\n"
            formatted_results += f"URL: {result.get('url', 'N/A')}\n"
            formatted_results += f"Snippet: {result.get('snippet', 'N/A')}\n\n"
        return formatted_results

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        formatted_results = f"Title: {results.get('title', 'N/A')}\n"
        formatted_results += f"URL: {results.get('url', 'N/A')}\n"
        formatted_results += f"Content: {results.get('content', 'N/A')}\n"
        return formatted_results
