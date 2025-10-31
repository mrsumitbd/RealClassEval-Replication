
import json
import requests
from typing import Any, Dict, Optional


class LocalBedrockAgentCoreClient:
    """Local Bedrock AgentCore client for invoking endpoints."""

    def __init__(self, endpoint: str):
        """
        Initialize the local client with the given endpoint.

        Parameters
        ----------
        endpoint : str
            The base URL of the local Bedrock AgentCore endpoint.
        """
        self.endpoint = endpoint.rstrip("/")

    def invoke_endpoint(
        self,
        session_id: str,
        payload: str,
        workload_access_token: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Invoke the Bedrock AgentCore endpoint with the provided session ID,
        payload, and workload access token.

        Parameters
        ----------
        session_id : str
            Identifier for the current session.
        payload : str
            The payload to send to the endpoint.
        workload_access_token : str
            Bearer token used for authentication.

        Returns
        -------
        dict or None
            Parsed JSON response from the endpoint if available; otherwise
            the raw text response. Returns None if the request fails.
        """
        url = f"{self.endpoint}/invoke"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {workload_access_token}",
        }
        body = {"session_id": session_id, "payload": payload}

        try:
            response = requests.post(
                url, headers=headers, json=body, timeout=30)
            response.raise_for_status()
        except requests.RequestException as exc:
            # Log the exception or handle it as needed
            print(f"Request failed: {exc}")
            return None

        try:
            return response.json()
        except ValueError:
            # Response is not JSON; return raw text
            return {"raw_response": response.text}
