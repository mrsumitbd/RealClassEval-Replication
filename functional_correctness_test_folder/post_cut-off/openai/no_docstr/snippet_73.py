
import json
import requests
from typing import List, Dict, Any


class BochaAISearchAPI:
    """
    A simple client for the Bocha AI Search API.
    """

    _BASE_URL = "https://api.bocha.ai"

    def __init__(self, api_key: str, max_results: int = 20):
        """
        Initialize the API client.

        :param api_key: The API key for authentication.
        :param max_results: Maximum number of results to return per request.
        """
        self.api_key = api_key
        self.max_results = max_results
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def search_web(self, query: str, summary: bool = True, freshness: str = "noLimit") -> List[Dict[str, Any]]:
        """
        Search the web for the given query.

        :param query: The search query string.
        :param summary: Whether to return a summary of each result.
        :param freshness: Freshness filter (e.g., 'noLimit', 'last24Hours', etc.).
        :return: A list of result dictionaries.
        """
        url = f"{self._BASE_URL}/search/web"
        body = {
            "query": query,
            "summary": summary,
            "maxResults": self.max_results,
            "freshness": freshness,
        }
        return self._post(url, body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness: str = "noLimit") -> List[Dict[str, Any]]:
        """
        Search the AI knowledge base for the given query.

        :param query: The search query string.
        :param answer: Whether to return a direct answer.
        :param stream: Whether to stream the response (ignored in this implementation).
        :param freshness: Freshness filter.
        :return: A list of result dictionaries.
        """
        url = f"{self._BASE_URL}/search/ai"
        body = {
            "query": query,
            "answer": answer,
            "stream": stream,
            "maxResults": self.max_results,
            "freshness": freshness,
        }
        return self._post(url, body)

    def _post(self, url: str, body: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Internal helper to perform a POST request.

        :param url: The full endpoint URL.
        :param body: The JSON body to send.
        :return: Parsed JSON response as a list of dictionaries.
        """
        try:
            response = requests.post(
                url, json=body, headers=self._headers, timeout=30)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"Request to {url} failed: {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"Invalid JSON response from {url}: {exc}") from exc

        # Normalise the response to a list of dicts
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            # If the API wraps results in a key, try to extract it
            if "results" in data and isinstance(data["results"], list):
                return data["results"]
            # Otherwise, return the dict as a single-item list
            return [data]
        raise RuntimeError(f"Unexpected response format from {url}: {data}")
