import requests
from typing import Any

class Mem0Client:

    def __init__(self, base_url: str='http://localhost:8000'):
        self.base_url = base_url

    def add(self, messages: list[dict], timestamp: str | None=None, user_id: str | None=None, agent_id: str | None=None, run_id: str | None=None, metadata: dict[str, Any] | None=None):
        """Create memories."""
        url = f'{self.base_url}/memories'
        if metadata is None:
            metadata = {}
        if user_id is None and agent_id is None and (run_id is None):
            raise ValueError('At least one of user_id, agent_id, or run_id must be provided.')
        if user_id:
            metadata['user_id'] = user_id
        if agent_id:
            metadata['agent_id'] = agent_id
        if run_id:
            metadata['run_id'] = run_id
        metadata['timestamp'] = timestamp
        data = {'messages': messages, 'user_id': user_id, 'agent_id': agent_id, 'run_id': run_id, 'metadata': metadata}
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def search(self, query: str, user_id: str | None=None, agent_id: str | None=None, run_id: str | None=None, filters: dict[str, Any] | None=None, top_k: int=10):
        """Search memories."""
        url = f'{self.base_url}/search'
        if filters is None:
            filters = {}
        data = {'query': query, 'user_id': user_id, 'agent_id': agent_id, 'run_id': run_id, 'filters': filters}
        response = requests.post(url, json=data)
        response.raise_for_status()
        results = response.json().get('results', [])
        top_k_results = results[:top_k] if len(results) > top_k else results
        relations = response.json().get('relations', [])
        top_k_relations = relations[:top_k] if len(relations) > top_k else relations
        return {'results': top_k_results, 'relations': top_k_relations}

    def get_all(self, user_id: str | None=None, agent_id: str | None=None, run_id: str | None=None):
        """Retrieve all memories."""
        url = f'{self.base_url}/memories'
        params = {}
        if user_id:
            params['user_id'] = user_id
        if agent_id:
            params['agent_id'] = agent_id
        if run_id:
            params['run_id'] = run_id
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get(self, memory_id: str):
        """Retrieve a specific memory by ID."""
        url = f'{self.base_url}/memories/{memory_id}'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def delete(self, memory_id: str):
        """Delete a specific memory by ID."""
        url = f'{self.base_url}/memories/{memory_id}'
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()

    def delete_all(self, user_id: str | None=None, agent_id: str | None=None, run_id: str | None=None):
        """Delete all memories for a user, agent, or run."""
        url = f'{self.base_url}/memories'
        params = {}
        if user_id:
            params['user_id'] = user_id
        if agent_id:
            params['agent_id'] = agent_id
        if run_id:
            params['run_id'] = run_id
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json()

    def reset(self):
        """Reset the memory store."""
        url = f'{self.base_url}/reset'
        response = requests.post(url)
        response.raise_for_status()
        return response.json()