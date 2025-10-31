import requests
from typing import Any, Dict, Optional


class LocalBedrockAgentCoreClient:
    """Local Bedrock AgentCore client for invoking endpoints."""

    def __init__(self, endpoint: str):
        """Initialize the local client with the given endpoint."""
        self._endpoint = endpoint.rstrip("/")
        self._session = requests.Session()
        self._timeout = 30

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str) -> Dict[str, Any]:
        """Invoke the endpoint with the given parameters."""
        url = self._endpoint
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if workload_access_token:
            headers["Authorization"] = f"Bearer {workload_access_token}"

        body = {
            "sessionId": session_id,
            "inputText": payload,
        }

        response = self._session.post(
            url, headers=headers, json=body, timeout=self._timeout)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {"result": response.text}
