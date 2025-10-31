import requests
import json
import logging

class LocalBedrockAgentCoreClient:
    """Local Bedrock AgentCore client for invoking endpoints."""

    def __init__(self, endpoint: str):
        """Initialize the local client with the given endpoint."""
        self.endpoint = endpoint
        self.logger = logging.getLogger('bedrock_agentcore.http_local')

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        """Invoke the endpoint with the given parameters."""
        from bedrock_agentcore.runtime.models import ACCESS_TOKEN_HEADER, SESSION_HEADER
        url = f'{self.endpoint}/invocations'
        headers = {'Content-Type': 'application/json', ACCESS_TOKEN_HEADER: workload_access_token, SESSION_HEADER: session_id}
        try:
            body = json.loads(payload) if isinstance(payload, str) else payload
        except json.JSONDecodeError:
            self.logger.warning('Failed to parse payload as JSON, wrapping in payload object')
            body = {'payload': payload}
        try:
            response = requests.post(url, headers=headers, json=body, timeout=900, stream=True)
            return _handle_http_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error('Failed to invoke agent endpoint: %s', str(e))
            raise