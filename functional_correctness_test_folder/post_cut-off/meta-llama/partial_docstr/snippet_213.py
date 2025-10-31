
import requests
import json


class LocalBedrockAgentCoreClient:
    '''Local Bedrock AgentCore client for invoking endpoints.'''

    def __init__(self, endpoint: str):
        '''Initialize the local client with the given endpoint.'''
        self.endpoint = endpoint

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {workload_access_token}'
        }
        data = {
            'sessionId': session_id,
            'payload': json.loads(payload)
        }
        response = requests.post(self.endpoint, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f'Failed to invoke endpoint. Status code: {response.status_code}, Response: {response.text}')
