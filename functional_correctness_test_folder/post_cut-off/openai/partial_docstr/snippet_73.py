
import json
import requests
from typing import List, Dict, Any


class BochaAISearchAPI:
    """BochaAI Search API Client"""

    _BASE_URL = "https://api.bocha.ai"

    def __init__(self, api_key: str, max_results: int = 20):
        """
        Initialize BochaAI Search API client.

        Args:
            api_key: BochaAI API key
            max_results: Maximum number of search results to retrieve
        """
        if not api_key:
            raise ValueError("api_key must be provided")
        if max_results <= 0:
            raise ValueError("max_results must be a positive integer")

        self.api_key = api_key
        self.max_results = max_results
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def search_web(self, query: str, summary: bool = True, freshness: str = "noLimit") -> List[Dict[str, Any]]:
        """
        Search the web for the given query.

        Args:
            query: Search query string
            summary: Whether to return a summary of each result
            freshness: Freshness filter (e.g., 'noLimit', 'last24Hours', etc.)

        Returns:
            List of result dictionaries
        """
        if not query:
            raise ValueError("query must be a non-empty string")

        body = {
            "query": query,
            "summary": summary,
            "max_results": self.max_results,
            "freshness": freshness,
        }
        url = f"{self._BASE_URL}/search/web"
        return self._post(url, body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness: str = "noLimit") -> List[Dict[str, Any]]:
        """
        Search AI knowledge base for the given query.

        Args:
            query: Search query string
            answer: Whether to return a direct answer
            stream: Whether to stream results (ignored in this implementation)
            freshness: Freshness filter

        Returns:
            List of result dictionaries
        """
        if not query:
            raise ValueError("query must be a non-empty string")

        body = {
            "query": query,
            "answer": answer,
            "stream": stream,
            "max_results": self.max_results,
            "freshness": freshness,
        }
        url = f"{self._BASE_URL}/search/ai"
        return self._post(url, body)

    def _post(self, url: str, body: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Send POST request and parse BochaAI search results.

        Args:
            url: Full endpoint URL
            body: JSON body to send

        Returns:
            List of result dictionaries

        Raises:
            RuntimeError: If the request fails or the response is invalid
        """
        try:
            response = requests.post(
                url, headers=self._headers, data=json.dumps(body), timeout=10)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"Request to {url} failed: {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(f"Invalid JSON response from {url}") from exc

        # Expecting the API to return a dict with a 'results' key
        if not isinstance(data, dict) or "results" not in data:
            raise RuntimeError(f"Unexpected response format from {url}")

        results = data["results"]
        if not isinstance(results, list):
            raise RuntimeError(
                f"Results should be a list, got {type(results)}")

        return results
