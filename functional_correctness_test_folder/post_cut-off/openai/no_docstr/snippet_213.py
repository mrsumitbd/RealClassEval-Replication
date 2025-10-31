
import json
import requests
from typing import Any, Dict


class LocalBedrockAgentCoreClient:
    """
    A simple HTTP client for invoking a local Bedrock Agent Core endpoint.
    """

    def __init__(self, endpoint: str):
        """
        Initialize the client with the base endpoint URL.

        Args:
            endpoint: The base URL of the Bedrock Agent Core service.
        """
        self.endpoint = endpoint.rstrip("/")
        self._session = requests.Session()

    def invoke_endpoint(
        self,
        session_id: str,
        payload: str,
        workload_access_token: str,
    ) -> Dict[str, Any]:
        """
        Invoke the Bedrock Agent Core endpoint with the given session ID,
        payload, and access token.

        Args:
            session_id: Identifier for the current session.
            payload: The request payload as a JSON string.
            workload_access_token: Bearer token for authentication.

        Returns:
            The JSON-decoded response from the service.

        Raises:
            requests.HTTPError: If the HTTP request returned an error status.
            requests.RequestException: For network-related errors.
            ValueError: If the response cannot be decoded as JSON.
        """
        url = f"{self.endpoint}/invoke"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {workload_access_token}",
        }

        # Prepare the request body
        try:
            body = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ValueError("Payload must be a valid JSON string") from exc

        body.update({"session_id": session_id})

        response = self._session.post(url, json=body, headers=headers)

        # Raise an exception for HTTP error codes
        response.raise_for_status()

        # Parse and return JSON response
        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise ValueError("Response is not valid JSON") from exc
