
import requests
from typing import Any


class LocalBedrockAgentCoreClient:
    """Local Bedrock AgentCore client for invoking endpoints."""

    def __init__(self, endpoint: str):
        """Initialize the local client with the given endpoint."""
        self.endpoint = endpoint

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        """Invoke the endpoint with the given parameters."""
        headers = {
            'Content-Type': 'application/json',
            'X-Amzn-Session-Id': session_id,
            'X-Amzn-Workload-Access-Token': workload_access_token
        }
        try:
            response = requests.post(
                self.endpoint, headers=headers, data=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to invoke endpoint: {e}") from e
        return response.json()
