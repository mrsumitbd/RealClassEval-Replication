
import requests
from typing import Any, Dict


class LocalBedrockAgentCoreClient:
    '''Local Bedrock AgentCore client for invoking endpoints.'''

    def __init__(self, endpoint: str):
        '''Initialize the local client with the given endpoint.'''
        self.endpoint = endpoint

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str) -> Dict[str, Any]:
        '''Invoke the endpoint with the given parameters.'''
        headers = {
            'Content-Type': 'application/json',
            'Session-Id': session_id,
            'Authorization': f'Bearer {workload_access_token}'
        }
        try:
            response = requests.post(
                self.endpoint, headers=headers, data=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            raise Exception(f'HTTP error occurred: {http_err}')
        except requests.exceptions.RequestException as req_err:
            raise Exception(f'Request error occurred: {req_err}')
        return response.json()
