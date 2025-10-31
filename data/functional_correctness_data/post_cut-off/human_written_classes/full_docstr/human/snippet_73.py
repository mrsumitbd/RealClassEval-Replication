import json
import requests

class BochaAISearchAPI:
    """BochaAI Search API Client"""

    def __init__(self, api_key: str, max_results: int=20):
        """
        Initialize BochaAI Search API client.

        Args:
            api_key: BochaAI API key
            max_results: Maximum number of search results to retrieve
        """
        self.api_key = api_key
        self.max_results = max_results
        self.web_url = 'https://api.bochaai.com/v1/web-search'
        self.ai_url = 'https://api.bochaai.com/v1/ai-search'
        self.headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

    def search_web(self, query: str, summary: bool=True, freshness='noLimit') -> list[dict]:
        """
        Perform a Web Search (equivalent to the first curl).

        Args:
            query: Search query string
            summary: Whether to include summary in the results
            freshness: Freshness filter (e.g. 'noLimit', 'day', 'week')

        Returns:
            A list of search result dicts
        """
        body = {'query': query, 'summary': summary, 'freshness': freshness, 'count': self.max_results}
        return self._post(self.web_url, body)

    def search_ai(self, query: str, answer: bool=False, stream: bool=False, freshness='noLimit') -> list[dict]:
        """
        Perform an AI Search (equivalent to the second curl).

        Args:
            query: Search query string
            answer: Whether BochaAI should generate an answer
            stream: Whether to use streaming response
            freshness: Freshness filter (e.g. 'noLimit', 'day', 'week')

        Returns:
            A list of search result dicts
        """
        body = {'query': query, 'freshness': freshness, 'count': self.max_results, 'answer': answer, 'stream': stream}
        return self._post(self.ai_url, body)

    def _post(self, url: str, body: dict) -> list[dict]:
        """Send POST request and parse BochaAI search results."""
        try:
            resp = requests.post(url, headers=self.headers, json=body)
            resp.raise_for_status()
            raw_data = resp.json()
            if 'messages' in raw_data:
                results = []
                for msg in raw_data['messages']:
                    if msg.get('type') == 'source' and msg.get('content_type') == 'webpage':
                        try:
                            content_json = json.loads(msg['content'])
                            results.extend(content_json.get('value', []))
                        except Exception as e:
                            logger.error(f'Failed to parse message content: {e}')
                return results
            return raw_data.get('data', {}).get('webPages', {}).get('value', [])
        except Exception:
            import traceback
            logger.error(f'BochaAI search error: {traceback.format_exc()}')
            return []