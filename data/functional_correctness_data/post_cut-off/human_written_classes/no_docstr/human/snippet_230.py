import requests

class MetadataAPIClient:

    def __init__(self, *, url: str, headers: dict[str, str]):
        self.url = url
        self.headers = headers

    def execute_query(self, query: str, variables: dict) -> dict:
        response = requests.post(url=self.url, json={'query': query, 'variables': variables}, headers=self.headers)
        return response.json()