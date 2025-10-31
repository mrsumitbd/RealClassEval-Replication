import os
import json
from typing import List, Dict
import requests


class BochaAISearchAPI:
    '''BochaAI Search API Client'''

    def __init__(self, api_key: str, max_results: int = 20):
        '''
        Initialize BochaAI Search API client.
        Args:
            api_key: BochaAI API key
            max_results: Maximum number of search results to retrieve
        '''
        if not api_key or not isinstance(api_key, str):
            raise ValueError('A valid BochaAI API key (string) is required.')
        self.api_key = api_key
        self.max_results = max_results
        self.base_url = os.getenv(
            'BOCHAAI_BASE_URL', 'https://api.bocha.ai/v1')
        self.web_search_url = f'{self.base_url}/search/web'
        self.ai_search_url = f'{self.base_url}/search/ai'
        self.timeout = float(os.getenv('BOCHAAI_TIMEOUT', '30'))

    def search_web(self, query: str, summary: bool = True, freshness: str = 'noLimit') -> List[Dict]:
        '''
        Perform a Web Search (equivalent to the first curl).
        Args:
            query: Search query string
            summary: Whether to include summary in the results
            freshness: Freshness filter (e.g. 'noLimit', 'day', 'week')
        Returns:
            A list of search result dicts
        '''
        if not query or not isinstance(query, str):
            raise ValueError('query must be a non-empty string.')
        body = {
            'query': query,
            'maxResults': self.max_results,
            'freshness': freshness,
            'summary': summary,
        }
        return self._post(self.web_search_url, body)

    def search_ai(self, query: str, answer: bool = False, stream: bool = False, freshness: str = 'noLimit') -> List[Dict]:
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
        if not query or not isinstance(query, str):
            raise ValueError('query must be a non-empty string.')
        body = {
            'query': query,
            'maxResults': self.max_results,
            'freshness': freshness,
            'answer': answer,
            'stream': stream,
        }
        return self._post(self.ai_search_url, body | {'stream': stream})

    def _post(self, url: str, body: dict) -> List[Dict]:
        '''Send POST request and parse BochaAI search results.'''
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        stream = bool(body.get('stream', False))
        if stream:
            headers['Accept'] = 'text/event-stream'

        try:
            resp = requests.post(url, headers=headers,
                                 json=body, timeout=self.timeout, stream=stream)
        except requests.RequestException as e:
            raise RuntimeError(f'Failed to connect to BochaAI API: {e}') from e

        if resp.status_code >= 400:
            content = resp.text
            try:
                content_json = resp.json()
                message = content_json.get(
                    'error') or content_json.get('message') or content
            except Exception:
                message = content
            raise requests.HTTPError(
                f'BochaAI API error {resp.status_code}: {message}', response=resp)

        def _extract(obj) -> List[Dict]:
            if obj is None:
                return []
            if isinstance(obj, list):
                return [i for i in obj if isinstance(i, dict)]
            if isinstance(obj, dict):
                for key in ('results', 'data', 'output', 'answers', 'items'):
                    v = obj.get(key)
                    if isinstance(v, list):
                        return [i for i in v if isinstance(i, dict)]
                return [obj]
            return []

        results: List[Dict] = []

        if stream:
            for raw_line in resp.iter_lines(decode_unicode=True):
                if not raw_line:
                    continue
                line = raw_line.strip()
                if line.startswith(':'):
                    continue
                if line.lower().startswith('data:'):
                    payload = line[5:].strip()
                else:
                    payload = line
                if payload in ('[DONE]', 'DONE'):
                    break
                try:
                    obj = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                results.extend(_extract(obj))
            return results

        try:
            data = resp.json()
        except ValueError:
            # Fallback if non-JSON but 2xx
            text = resp.text.strip()
            try:
                data = json.loads(text)
            except Exception:
                return []
        return _extract(data)
