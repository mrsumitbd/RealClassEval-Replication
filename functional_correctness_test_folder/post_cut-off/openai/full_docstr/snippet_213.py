
import json
import requests
from typing import Any, Dict, Union


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
    ) -> Union[Dict[str, Any], str]:
        """
        Invoke the endpoint with the given parameters.

        Parameters
        ----------
        session_id : str
            Identifier for the current session.
        payload : str
            The payload to send to the endpoint (JSON string).
        workload_access_token : str
            Bearer token used for authentication.

        Returns
        -------
        Union[Dict[str, Any], str]
            Parsed JSON response if the response content type is JSON,
            otherwise the raw text response.

        Raises
        ------
        RuntimeError
            If the request fails or the endpoint returns a non‑2xx status code.
        """
        url = self.endpoint
        headers = {
            "Authorization": f"Bearer {workload_access_token}",
            "Content-Type": "application/json",
            "X-Session-Id": session_id,
        }

        # Ensure payload is a JSON string; if it's already a dict, convert it.
        if isinstance(payload, str):
            try:
                payload_data = json.loads(payload)
            except json.JSONDecodeError:
                # Treat as raw string if not valid JSON
                payload_data = {"payload": payload}
        else:
            payload_data = payload

        try:
            response = requests.post(
                url=url,
                json=payload_data,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(
                f"Failed to invoke endpoint '{url}': {exc}"
            ) from exc

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type.lower():
            try:
                return response.json()
            except ValueError:
                # Fallback to raw text if JSON parsing fails
                return response.text
        return response.text
