
import requests
import json


class BochaAISearchAPI:

    def __init__(self, api_key: str, max_results: int = 20):
        self.api_key = api_key
        self.max_results = max_results
        self.base_url = 'https://api.bochaai.com/v1'

    def search_web(self, query: str, summary: bool = True, freshness='noLimit') -> list[dict]:
        url = f'{self.base_url}/search/web'
        body = {
            'query': query,
            'summary': summary,
            'freshness': freshness,
            'maxResults': self.max_results
        }
        return self._post(url, body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness='noLimit') -> list[dict]:
        url = f'{self.base_url}/search/ai'
        body = {
            'query': query,
            'answer': answer,
            'stream': stream,
            'freshness': freshness,
            'maxResults': self.max_results
        }
        return self._post(url, body)

    def _post(self, url: str, body: dict) -> list[dict]:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f'Failed to retrieve data. Status code: {response.status_code}')
