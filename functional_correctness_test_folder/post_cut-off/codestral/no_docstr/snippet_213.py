
import requests


class LocalBedrockAgentCoreClient:

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
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
