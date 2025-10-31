
import requests


class LocalBedrockAgentCoreClient:

    def __init__(self, endpoint: str):
        self.endpoint = endpoint.rstrip('/')

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        url = f"{self.endpoint}/invoke"
        headers = {
            "Authorization": f"Bearer {workload_access_token}",
            "Content-Type": "application/json",
            "X-Session-Id": session_id
        }
        data = {
            "payload": payload
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
