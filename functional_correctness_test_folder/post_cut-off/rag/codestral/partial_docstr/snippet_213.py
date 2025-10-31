
import requests
from typing import Any


class LocalBedrockAgentCoreClient:
    '''Local Bedrock AgentCore client for invoking endpoints.'''

    def __init__(self, endpoint: str):
        '''Initialize the local client with the given endpoint.'''
        self.endpoint = endpoint

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        '''Invoke the endpoint with the given parameters.'''
        headers = {
            'Authorization': f'Bearer {workload_access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'session_id': session_id,
            'payload': payload
        }
        response = requests.post(self.endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
