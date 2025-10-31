
import requests
from typing import List, Dict, Any


class BochaAISearchAPI:
    '''BochaAI Search API Client'''

    _BASE_URL = "https://api.bocha.ai"

    def __init__(self, api_key: str, max_results: int = 20):
        '''
        Initialize BochaAI Search API client.
        Args:
            api_key: BochaAI API key
            max_results: Maximum number of search results to retrieve
        '''
        self.api_key = api_key
        self.max_results = max_results
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def search_web(self, query: str, summary: bool = True, freshness: str = 'noLimit') -> List[Dict[str, Any]]:
        '''
        Perform a Web Search (equivalent to the first curl).
        Args:
            query: Search query string
            summary: Whether to include summary in the results
            freshness: Freshness filter (e.g. 'noLimit', 'day', 'week')
        Returns:
            A list of search result dicts
        '''
        body = {
            "query": query,
            "summary": summary,
            "freshness": freshness,
            "max_results": self.max_results,
        }
        url = f"{self._BASE_URL}/search/web"
        return self._post(url, body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness: str = 'noLimit') -> List[Dict[str, Any]]:
        '''
        Perform an AI Search (equivalent to the second curl).
        Args:
            query: Search query string
            answer: Whether BochaAI should generate an answer
            stream: Whether to use streaming response
            freshness: Freshness filter (e.g. 'noLimit', 'day', 'week')
        Returns:
            A list of search result dicts
        '''
        body = {
            "query": query,
            "answer": answer,
            "stream": stream,
            "freshness": freshness,
            "max_results": self.max_results,
        }
        url = f"{self._BASE_URL}/search/ai"
        return self._post(url, body)

    def _post(self, url: str, body: Dict[str, Any]) -> List[Dict[str, Any]]:
        '''Send POST request and parse BochaAI search results.'''
        try:
            response = requests.post(
                url, json=body, headers=self._headers, timeout=30)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"BochaAI API request failed: {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Invalid JSON response from BochaAI API") from exc

        # The API is expected to return a top‑level key `results` containing a list.
        # If that key is missing, fall back to the whole payload.
        return data.get("results", data)
