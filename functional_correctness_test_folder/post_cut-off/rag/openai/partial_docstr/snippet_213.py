
import json
import requests
from typing import Any, Dict


class LocalBedrockAgentCoreClient:
    """Local Bedrock AgentCore client for invoking endpoints."""

    def __init__(self, endpoint: str):
        """
        Initialize the local client with the given endpoint.

        Parameters
        ----------
        endpoint : str
            The base URL of the Bedrock AgentCore service.
        """
        # Ensure the endpoint ends with a slash so that paths can be appended
        self._endpoint = endpoint.rstrip("/") + "/"

    def invoke_endpoint(
        self,
        session_id: str,
        payload: str,
        workload_access_token: str,
    ) -> Dict[str, Any]:
        """
        Invoke the endpoint with the given parameters.

        Parameters
        ----------
        session_id : str
            The session identifier to be sent in the request header.
        payload : str
            The JSON payload to send in the request body.
        workload_access_token : str
            The bearer token used for authentication.

        Returns
        -------
        dict
            The JSON-decoded response from the service.

        Raises
        ------
        requests.exceptions.HTTPError
            If the HTTP request returned an unsuccessful status code.
        requests.exceptions.ConnectionError
            If a network problem occurred.
        requests.exceptions.Timeout
            If the request timed out.
        requests.exceptions.RequestException
            For any other request-related errors.
        """
        url = self._endpoint + \
            "invoke"  # The actual path may vary; adjust as needed.
        headers = {
            "Content-Type": "application/json",
            "Session-Id": session_id,
            "Authorization": f"Bearer {workload_access_token}",
        }

        try:
            response = requests.post(
                url, headers=headers, data=payload, timeout=10
            )
            response.raise_for_status()
            # The service is expected to return JSON
            return response.json()
        except requests.exceptions.HTTPError as err:
            # Re‑raise HTTP errors with a clearer message
            raise requests.exceptions.HTTPError(
                f"HTTP error while invoking endpoint: {err}"
            ) from err
        except requests.exceptions.ConnectionError as err:
            raise requests.exceptions.ConnectionError(
                f"Connection error while invoking endpoint: {err}"
            ) from err
        except requests.exceptions.Timeout as err:
            raise requests.exceptions.Timeout(
                f"Timeout while invoking endpoint: {err}"
            ) from err
        except requests.exceptions.RequestException as err:
            raise requests.exceptions.RequestException(
                f"Request exception while invoking endpoint: {err}"
            ) from err
