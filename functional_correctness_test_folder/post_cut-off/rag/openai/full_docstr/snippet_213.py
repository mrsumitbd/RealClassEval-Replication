
import json
import logging
from typing import Any, Dict

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

_LOGGER = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10  # seconds


class LocalBedrockAgentCoreClient:
    """Local Bedrock AgentCore client for invoking endpoints."""

    def __init__(self, endpoint: str):
        """Initialize the local client with the given endpoint."""
        self._endpoint = endpoint.rstrip("/")

    def invoke_endpoint(
        self,
        session_id: str,
        payload: str,
        workload_access_token: str,
    ) -> Dict[str, Any]:
        """Invoke the endpoint with the given parameters.

        Args:
            session_id: The session identifier for the request.
            payload: The request payload as a JSON string.
            workload_access_token: Bearer token for authentication.

        Returns:
            The JSON-decoded response from the endpoint.

        Raises:
            ConnectionError: If the request fails due to network issues.
            Timeout: If the request times out.
            RequestException: For other request-related errors.
        """
        url = f"{self._endpoint}/invoke"
        headers = {
            "Authorization": f"Bearer {workload_access_token}",
            "Content-Type": "application/json",
            "X-Session-Id": session_id,
        }

        try:
            _LOGGER.debug(
                "Invoking Bedrock AgentCore endpoint %s with session %s", url, session_id)
            response = requests.post(
                url,
                headers=headers,
                data=payload,
                timeout=DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
        except HTTPError as err:
            _LOGGER.error(
                "HTTP error while invoking Bedrock AgentCore: %s", err)
            raise
        except ConnectionError as err:
            _LOGGER.error(
                "Connection error while invoking Bedrock AgentCore: %s", err)
            raise
        except Timeout as err:
            _LOGGER.error("Timeout while invoking Bedrock AgentCore: %s", err)
            raise
        except RequestException as err:
            _LOGGER.error(
                "Request exception while invoking Bedrock AgentCore: %s", err)
            raise

        try:
            return response.json()
        except ValueError as err:
            _LOGGER.error("Failed to decode JSON response: %s", err)
            raise
