
import requests
from typing import List, Dict, Optional, Union


class BochaAISearchAPI:
    '''BochaAI Search API Client'''

    def __init__(self, api_key: str, max_results: int = 20):
        '''
        Initialize BochaAI Search API client.
        Args:
            api_key: BochaAI API key
            max_results: Maximum number of search results to retrieve
        '''
        self.api_key = api_key
        self.max_results = max_results
        self.base_url = "https://api.bocha.ai/search"

    def search_web(self, query: str, summary: bool = True, freshness: str = 'noLimit') -> List[Dict]:
        '''
        Search the web using BochaAI.
        Args:
            query: Search query
            summary: Whether to include a summary of the results
            freshness: Time limit for results ('noLimit', 'day', 'week', 'month')
        Returns:
            List of search results as dictionaries
        '''
        body = {
            "query": query,
            "max_results": self.max_results,
            "summary": summary,
            "freshness": freshness,
            "type": "web"
        }
        return self._post(f"{self.base_url}/web", body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness: str = 'noLimit') -> List[Dict]:
        '''
        Search using BochaAI's AI models.
        Args:
            query: Search query
            answer: Whether to generate an answer
            stream: Whether to stream results
            freshness: Time limit for results ('noLimit', 'day', 'week', 'month')
        Returns:
            List of search results as dictionaries
        '''
        body = {
            "query": query,
            "max_results": self.max_results,
            "answer": answer,
            "stream": stream,
            "freshness": freshness,
            "type": "ai"
        }
        return self._post(f"{self.base_url}/ai", body)

    def _post(self, url: str, body: dict) -> List[Dict]:
        '''Send POST request and parse BochaAI search results.'''
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
