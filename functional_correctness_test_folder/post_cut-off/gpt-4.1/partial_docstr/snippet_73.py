
import requests


class BochaAISearchAPI:
    '''BochaAI Search API Client'''
    BASE_URL = "https://api.bocha.ai/v1/search"

    def __init__(self, api_key: str, max_results: int = 20):
        '''
        Initialize BochaAI Search API client.
        Args:
            api_key: BochaAI API key
            max_results: Maximum number of search results to retrieve
        '''
        self.api_key = api_key
        self.max_results = max_results
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def search_web(self, query: str, summary: bool = True, freshness='noLimit') -> list[dict]:
        body = {
            "query": query,
            "type": "web",
            "summary": summary,
            "freshness": freshness,
            "maxResults": self.max_results
        }
        url = f"{self.BASE_URL}/web"
        return self._post(url, body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness='noLimit') -> list[dict]:
        body = {
            "query": query,
            "type": "ai",
            "answer": answer,
            "stream": stream,
            "freshness": freshness,
            "maxResults": self.max_results
        }
        url = f"{self.BASE_URL}/ai"
        return self._post(url, body)

    def _post(self, url: str, body: dict) -> list[dict]:
        '''Send POST request and parse BochaAI search results.'''
        response = requests.post(url, json=body, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and "results" in data:
            return data["results"]
        elif isinstance(data, list):
            return data
        else:
            return []
