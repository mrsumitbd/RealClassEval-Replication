from typing import Dict, List, Optional
import requests
from concurrent.futures import ThreadPoolExecutor

class OnlineSearchEngine:

    def __init__(self, config):
        self.config = config

    def _search_query(self, query: str):
        params = {'engine': self.config.serp_engine, 'q': query, 'api_key': self.config.serp_api_key}
        response = requests.get(self.config.search_url, params=params)
        return response.json()

    def batch_search(self, queries: List[str]):
        results = []
        with ThreadPoolExecutor() as executor:
            for result in executor.map(self._search_query, queries):
                results.append(self._process_result(result))
        return results

    def _process_result(self, search_result: Dict):
        results = []
        answer_box = search_result.get('answer_box', {})
        if answer_box:
            title = answer_box.get('title', 'No title.')
            snippet = answer_box.get('snippet', 'No snippet available.')
            results.append({'document': {'contents': f'"{title}"\n{snippet}'}})
        organic_results = search_result.get('organic_results', [])
        for _, result in enumerate(organic_results[:self.config.topk]):
            title = result.get('title', 'No title.')
            snippet = result.get('snippet', 'No snippet available.')
            results.append({'document': {'contents': f'"{title}"\n{snippet}'}})
        related_results = search_result.get('related_questions', [])
        for _, result in enumerate(related_results[:self.config.topk]):
            title = result.get('question', 'No title.')
            snippet = result.get('snippet', 'No snippet available.')
            results.append({'document': {'contents': f'"{title}"\n{snippet}'}})
        return results