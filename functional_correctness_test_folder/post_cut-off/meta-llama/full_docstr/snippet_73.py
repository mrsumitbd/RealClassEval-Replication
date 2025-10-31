
import requests
import json


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
        self.base_url = 'https://api.bocha.ai/search'

    def search_web(self, query: str, summary: bool = True, freshness='noLimit') -> list[dict]:
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
            'query': query,
            'summary': summary,
            'freshness': freshness,
            'maxResults': self.max_results,
            'type': 'web'
        }
        return self._post(f'{self.base_url}/web', body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness='noLimit') -> list[dict]:
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
            'query': query,
            'answer': answer,
            'stream': stream,
            'freshness': freshness,
            'maxResults': self.max_results,
            'type': 'ai'
        }
        return self._post(f'{self.base_url}/ai', body)

    def _post(self, url: str, body: dict) -> list[dict]:
        '''Send POST request and parse BochaAI search results.'''
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=json.dumps(body))
        response.raise_for_status()
        return response.json().get('results', [])
