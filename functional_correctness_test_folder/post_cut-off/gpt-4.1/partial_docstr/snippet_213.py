
class LocalBedrockAgentCoreClient:
    '''Local Bedrock AgentCore client for invoking endpoints.'''

    def __init__(self, endpoint: str):
        '''Initialize the local client with the given endpoint.'''
        self.endpoint = endpoint

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        import requests

        headers = {
            'Authorization': f'Bearer {workload_access_token}',
            'Content-Type': 'application/json',
            'X-Session-Id': session_id
        }
        data = {
            'payload': payload
        }
        response = requests.post(self.endpoint, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
