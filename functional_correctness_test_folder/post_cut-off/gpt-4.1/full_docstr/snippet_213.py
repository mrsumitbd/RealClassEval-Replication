
import json
import os


class LocalBedrockAgentCoreClient:
    '''Local Bedrock AgentCore client for invoking endpoints.'''

    def __init__(self, endpoint: str):
        '''Initialize the local client with the given endpoint.'''
        self.endpoint = endpoint

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        '''Invoke the endpoint with the given parameters.'''
        # Simulate local endpoint invocation by reading a file or returning a mock response
        # For demonstration, if endpoint is a file path, read and return its content as JSON
        if os.path.isfile(self.endpoint):
            with open(self.endpoint, 'r', encoding='utf-8') as f:
                data = f.read()
            return {
                "session_id": session_id,
                "payload": payload,
                "workload_access_token": workload_access_token,
                "endpoint_response": data
            }
        else:
            # Return a mock response
            return {
                "session_id": session_id,
                "payload": payload,
                "workload_access_token": workload_access_token,
                "endpoint": self.endpoint,
                "status": "invoked"
            }
