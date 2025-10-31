
import requests
from typing import List, Dict


class BochaAISearchAPI:

    def __init__(self, api_key: str, max_results: int = 20):
        self.api_key = api_key
        self.max_results = max_results
        self.base_url = "https://api.bocha.ai/v1"

    def search_web(self, query: str, summary: bool = True, freshness: str = 'noLimit') -> List[Dict]:
        endpoint = f"{self.base_url}/search/web"
        body = {
            "query": query,
            "summary": summary,
            "freshness": freshness,
            "max_results": self.max_results
        }
        return self._post(endpoint, body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness: str = 'noLimit') -> List[Dict]:
        endpoint = f"{self.base_url}/search/ai"
        body = {
            "query": query,
            "answer": answer,
            "stream": stream,
            "freshness": freshness,
            "max_results": self.max_results
        }
        return self._post(endpoint, body)

    def _post(self, url: str, body: Dict) -> List[Dict]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        return response.json()
