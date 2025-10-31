class LocalBedrockAgentCoreClient:
    '''Local Bedrock AgentCore client for invoking endpoints.'''

    def __init__(self, endpoint: str):
        '''Initialize the local client with the given endpoint.'''
        self.endpoint = endpoint

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        '''Invoke the endpoint with the given parameters.'''
        import requests

        headers = {
            "Authorization": f"Bearer {workload_access_token}",
            "Content-Type": "application/json",
            "x-amz-bedrock-agent-session-id": session_id,
        }
        response = requests.post(
            self.endpoint,
            headers=headers,
            data=payload
        )
        response.raise_for_status()
        return response.json()
