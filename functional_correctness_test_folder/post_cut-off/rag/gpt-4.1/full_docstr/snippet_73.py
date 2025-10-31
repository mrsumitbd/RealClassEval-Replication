import requests


class BochaAISearchAPI:
    '''BochaAI Search API Client'''

    BASE_URL = "https://api.bocha.ai/v1"

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
        '''
        Perform a Web Search (equivalent to the first curl).
        Args:
            query: Search query string
            summary: Whether to include summary in the results
            freshness: Freshness filter (e.g. 'noLimit', 'day', 'week')
        Returns:
            A list of search result dicts
        '''
        url = f"{self.BASE_URL}/search/web"
        body = {
            "query": query,
            "summary": summary,
            "freshness": freshness,
            "maxResults": self.max_results
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
        url = f"{self.BASE_URL}/search/ai"
        body = {
            "query": query,
            "answer": answer,
            "stream": stream,
            "freshness": freshness,
            "maxResults": self.max_results
        }
        return self._post(url, body)

    def _post(self, url: str, body: dict) -> list[dict]:
        '''Send POST request and parse BochaAI search results.'''
        response = requests.post(url, headers=self.headers, json=body)
        response.raise_for_status()
        data = response.json()
        # The API returns results in a 'results' key, or the whole response is a list
        if isinstance(data, dict) and "results" in data:
            return data["results"]
        elif isinstance(data, list):
            return data
        else:
            return [data] if data else []
