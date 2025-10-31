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
        self.api_key = api_key
        self.max_results = max_results
        self.base_url = 'https://api.bocha.ai/v1'
        self.timeout = 30
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })

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
        url = f'{self.base_url}/search/web'
        body = {
            'query': query,
            'summary': summary,
            'freshness': freshness,
            'size': self.max_results,
            'limit': self.max_results,
        }
        return self._post(url, body)

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
        url = f'{self.base_url}/search/ai'
        body = {
            'query': query,
            'answer': answer,
            'stream': stream,
            'freshness': freshness,
            'size': self.max_results,
            'limit': self.max_results,
        }
        return self._post(url, body)

    def _post(self, url: str, body: dict) -> list[dict]:
        '''Send POST request and parse BochaAI search results.'''
        try:
            if body.get('stream'):
                with self.session.post(url, json=body, timeout=self.timeout, stream=True) as r:
                    r.raise_for_status()
                    aggregated: List[Dict] = []
                    for line in r.iter_lines(decode_unicode=True):
                        if not line:
                            continue
                        data_str = line
                        if data_str.startswith('data:'):
                            data_str = data_str[len('data:'):].strip()
                        if data_str.strip() in ('', '[DONE]'):
                            continue
                        try:
                            chunk = json.loads(data_str)
                        except json.JSONDecodeError:
                            continue
                        # If chunk contains a list of results
                        if isinstance(chunk, dict):
                            if 'results' in chunk and isinstance(chunk['results'], list):
                                aggregated.extend(
                                    self._ensure_list_of_dicts(chunk['results']))
                            elif 'data' in chunk and isinstance(chunk['data'], list):
                                aggregated.extend(
                                    self._ensure_list_of_dicts(chunk['data']))
                            else:
                                aggregated.append(chunk if isinstance(
                                    chunk, dict) else {'value': chunk})
                        elif isinstance(chunk, list):
                            aggregated.extend(
                                self._ensure_list_of_dicts(chunk))
                        else:
                            aggregated.append({'value': chunk})
                    return aggregated
            else:
                r = self.session.post(url, json=body, timeout=self.timeout)
                r.raise_for_status()
                payload = r.json()
                if isinstance(payload, list):
                    return self._ensure_list_of_dicts(payload)
                if isinstance(payload, dict):
                    if 'results' in payload and isinstance(payload['results'], list):
                        return self._ensure_list_of_dicts(payload['results'])
                    if 'data' in payload and isinstance(payload['data'], list):
                        return self._ensure_list_of_dicts(payload['data'])
                    if 'value' in payload and isinstance(payload['value'], list):
                        return self._ensure_list_of_dicts(payload['value'])
                    return [payload]
                return [{'value': payload}]
        except requests.RequestException as e:
            raise RuntimeError(f'BochaAI request failed: {e}') from e
        except ValueError as e:
            raise RuntimeError(f'Invalid response from BochaAI: {e}') from e

    @staticmethod
    def _ensure_list_of_dicts(items: list) -> list[dict]:
        normalized: List[Dict] = []
        for item in items:
            if isinstance(item, dict):
                normalized.append(item)
            else:
                normalized.append({'value': item})
        return normalized
