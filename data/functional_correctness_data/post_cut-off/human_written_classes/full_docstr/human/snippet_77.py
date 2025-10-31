import json
import uuid
import requests

class XinyuSearchAPI:
    """Xinyu Search API Client"""

    def __init__(self, access_key: str, search_engine_id: str, max_results: int=20):
        """
        Initialize Xinyu Search API client

        Args:
            access_key: Xinyu API access key
            max_results: Maximum number of results to retrieve
        """
        self.access_key = access_key
        self.max_results = max_results
        self.config = {'url': search_engine_id}
        self.headers = {'User-Agent': 'PostmanRuntime/7.39.0', 'Content-Type': 'application/json', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive', 'token': access_key}

    def query_detail(self, body: dict | None=None, detail: bool=True) -> list[dict]:
        """
        Query Xinyu search API for detailed results

        Args:
            body: Search parameters
            detail: Whether to get detailed results

        Returns:
            List of search results
        """
        res = []
        try:
            url = self.config['url']
            params = json.dumps(body)
            resp = requests.request('POST', url, headers=self.headers, data=params)
            res = json.loads(resp.text)['results']
            if 'search_type' in body:
                res = res['online']
            if not detail:
                for res_i in res:
                    res_i['summary'] = '「SUMMARY」' + res_i.get('summary', '')
        except Exception:
            import traceback
            logger.error(f'xinyu search error: {traceback.format_exc()}')
        return res

    def search(self, query: str, max_results: int | None=None) -> list[dict]:
        """
        Execute search request

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            List of search results
        """
        if max_results is None:
            max_results = self.max_results
        body = {'search_type': ['online'], 'online_search': {'max_entries': max_results, 'cache_switch': False, 'baidu_field': {'switch': False, 'mode': 'relevance', 'type': 'page'}, 'bing_field': {'switch': True, 'mode': 'relevance', 'type': 'page'}, 'sogou_field': {'switch': False, 'mode': 'relevance', 'type': 'page'}}, 'request_id': 'memos' + str(uuid.uuid4()), 'queries': query}
        return self.query_detail(body)