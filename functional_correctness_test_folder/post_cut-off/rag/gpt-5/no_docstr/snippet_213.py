import requests
from typing import Any, Union


class LocalBedrockAgentCoreClient:
    '''Local Bedrock AgentCore client for invoking endpoints.'''

    def __init__(self, endpoint: str):
        '''Initialize the local client with the given endpoint.'''
        if not endpoint or not isinstance(endpoint, str):
            raise ValueError('A valid endpoint string must be provided')
        self._endpoint = endpoint.rstrip('/')

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str) -> Union[dict[str, Any], str]:
        '''Invoke the endpoint with the given parameters.'''
        if not session_id or not isinstance(session_id, str):
            raise ValueError('A valid session_id must be provided')
        if not isinstance(payload, str):
            raise ValueError('payload must be a string')

        url = self._endpoint
        if not url.endswith('/invoke'):
            url = f'{url}/invoke'

        headers = {
            'Content-Type': 'application/json',
            'x-session-id': session_id,
        }
        if workload_access_token:
            headers['Authorization'] = f'Bearer {workload_access_token}'
            headers['x-amzn-bedrock-workload-token'] = workload_access_token

        body = {
            'sessionId': session_id,
            'inputText': payload,
        }

        response = requests.post(url, headers=headers, json=body, timeout=30)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type.lower():
            return response.json()
        return response.text
