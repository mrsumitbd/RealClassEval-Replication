
from typing import List, Dict, Any
import requests


class TavilySearchService:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.tavily.com/search"
        self.extract_api_url = "https://api.tavily.com/extract"

    def search(self, query: str, search_depth: str = 'basic', topic: str = 'general', include_domains: List[str] | None = None, exclude_domains: List[str] | None = None, max_results: int = 5) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth,
            "topic": topic,
            "max_results": max_results
        }
        if include_domains:
            data["include_domains"] = include_domains
        if exclude_domains:
            data["exclude_domains"] = exclude_domains

        response = requests.post(self.api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to retrieve search results. Status code: {response.status_code}")

    def extract(self, url: str) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "api_key": self.api_key,
            "url": url
        }

        response = requests.post(self.extract_api_url,
                                 headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to extract content from URL. Status code: {response.status_code}")

    def format_search_results(self, results: Dict[str, Any]) -> str:
        formatted_results = ""
        for result in results.get("results", []):
            formatted_results += f"Title: {result.get('title')}\n"
            formatted_results += f"URL: {result.get('url')}\n"
            formatted_results += f"Content: {result.get('content')}\n\n"
        return formatted_results

    def format_extract_results(self, results: Dict[str, Any]) -> str:
        return results.get("content", "")


# Example usage:
if __name__ == "__main__":
    api_key = "your_tavily_api_key"
    service = TavilySearchService(api_key)
    search_results = service.search("example search query")
    print(service.format_search_results(search_results))
    extract_results = service.extract("https://example.com")
    print(service.format_extract_results(extract_results))
