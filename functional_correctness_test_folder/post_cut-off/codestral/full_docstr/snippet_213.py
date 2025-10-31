
import requests


class LocalBedrockAgentCoreClient:
    '''Local Bedrock AgentCore client for invoking endpoints.'''

    def __init__(self, endpoint: str):
        '''Initialize the local client with the given endpoint.'''
        self.endpoint = endpoint

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        '''Invoke the endpoint with the given parameters.'''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {workload_access_token}'
        }
        data = {
            'session_id': session_id,
            'payload': payload
        }
        response = requests.post(self.endpoint, headers=headers, json=data)
        return response.json()
