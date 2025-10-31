import os
from tavily import TavilyClient

class TavilySearch:

    def __init__(self):
        api_key = os.getenv('TAVILY_API_KEY')
        if api_key:
            self.client = TavilyClient(api_key=api_key)
        else:
            self.client = None

    def search(self, query: str) -> str:
        """Perform a web search using the Tavily API and return a summary of results."""
        try:
            response = self.client.search(query=query, search_depth='advanced')
            results = response.get('results', [])
            summary = []
            for res in results:
                summary.append(f"Title: {res.get('title')}\nURL: {res.get('url')}\nContent: {res.get('content')}\n---")
            return '\n'.join(summary) if summary else 'No results found.'
        except Exception as e:
            return f'An unexpected error occurred during search: {e}'