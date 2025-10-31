
import requests
import json


class LocalBedrockAgentCoreClient:

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {workload_access_token}'
        }
        data = json.dumps({
            'sessionId': session_id,
            'payload': json.loads(payload)
        })
        response = requests.post(self.endpoint, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f'Failed to invoke endpoint. Status code: {response.status_code}, Response: {response.text}')
