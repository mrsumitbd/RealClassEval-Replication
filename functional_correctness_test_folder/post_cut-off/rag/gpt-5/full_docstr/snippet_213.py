import json
from typing import Any, Union

import requests
from requests.exceptions import HTTPError, RequestException, Timeout


class LocalBedrockAgentCoreClient:
    """Local Bedrock AgentCore client for invoking endpoints."""

    def __init__(self, endpoint: str):
        """Initialize the local client with the given endpoint."""
        if not endpoint or not isinstance(endpoint, str):
            raise ValueError("endpoint must be a non-empty string")
        self._endpoint = endpoint.rstrip("/")

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str) -> Union[dict[str, Any], str]:
        """Invoke the endpoint with the given parameters."""
        if not workload_access_token:
            raise ValueError("workload_access_token must be provided")
        headers = {
            "Authorization": f"Bearer {workload_access_token}",
            "Content-Type": "application/json",
        }
        if session_id:
            headers["X-Session-Id"] = session_id

        body = {"sessionId": session_id, "payload": payload}

        try:
            resp = requests.post(
                self._endpoint, headers=headers, json=body, timeout=30)
            resp.raise_for_status()
        except HTTPError as e:
            raise ConnectionError(
                f"HTTP error while invoking endpoint: {e}") from e
        except Timeout as e:
            raise TimeoutError(f"Timeout while invoking endpoint: {e}") from e
        except RequestException as e:
            raise ConnectionError(
                f"Request error while invoking endpoint: {e}") from e
        except Exception as e:
            raise RuntimeError(
                f"Unexpected error while invoking endpoint: {e}") from e

        content_type = resp.headers.get("Content-Type", "")
        if "application/json" in content_type:
            try:
                return resp.json()
            except ValueError:
                # Fallback if server mislabeled content type
                pass
        return resp.text
