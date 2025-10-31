
import logging
from typing import Any, cast

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

_LOGGER = logging.getLogger(__name__)

DEFAULT_REQUEST_TIMEOUT = 10  # seconds


class LocalBedrockAgentCoreClient:
    """Local Bedrock AgentCore client for invoking endpoints."""

    def __init__(self, endpoint: str):
        """Initialize the local client with the given endpoint."""
        # Ensure the endpoint does not end with a trailing slash
        self._endpoint = endpoint.rstrip("/")
        if not self._endpoint:
            raise ValueError("Endpoint must not be empty")

    def invoke_endpoint(
        self,
        session_id: str,
        payload: str,
        workload_access_token: str,
    ) -> dict[str, Any]:
        """Invoke the endpoint with the given parameters."""
        url = f"{self._endpoint}/invoke"
        headers = {
            "Content-Type": "application/json",
            "Session-Id": session_id,
            "Authorization": f"Bearer {workload_access_token}",
        }

        try:
            _LOGGER.debug("Invoking Bedrock AgentCore endpoint %s", url)
            response = requests.post(
                url, headers=headers, data=payload, timeout=DEFAULT_REQUEST_TIMEOUT
            )
            response.raise_for_status()
        except HTTPError as err:
            _LOGGER.debug("HTTP error while invoking endpoint: %s", err)
            raise
        except ConnectionError as err:
            _LOGGER.debug("Connection error while invoking endpoint: %s", err)
            raise
        except Timeout as err:
            _LOGGER.debug("Timeout while invoking endpoint: %s", err)
            raise
        except RequestException as err:
            _LOGGER.debug("Request exception while invoking endpoint: %s", err)
            raise
        except Exception as err:
            _LOGGER.debug("Unexpected error while invoking endpoint: %s", err)
            raise

        try:
            return cast(dict[str, Any], response.json())
        except ValueError as err:
            _LOGGER.debug("Failed to parse JSON response: %s", err)
            raise
