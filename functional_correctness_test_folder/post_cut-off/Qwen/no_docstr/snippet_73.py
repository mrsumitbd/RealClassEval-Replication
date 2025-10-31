
import requests


class BochaAISearchAPI:

    def __init__(self, api_key: str, max_results: int = 20):
        self.api_key = api_key
        self.max_results = max_results
        self.base_url = "https://api.bocha.ai/search"

    def search_web(self, query: str, summary: bool = True, freshness='noLimit') -> list[dict]:
        url = f"{self.base_url}/web"
        body = {
            "query": query,
            "summary": summary,
            "freshness": freshness,
            "max_results": self.max_results
        }
        return self._post(url, body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness='noLimit') -> list[dict]:
        url = f"{self.base_url}/ai"
        body = {
            "query": query,
            "answer": answer,
            "stream": stream,
            "freshness": freshness,
            "max_results": self.max_results
        }
        return self._post(url, body)

    def _post(self, url: str, body: dict) -> list[dict]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        return response.json()
