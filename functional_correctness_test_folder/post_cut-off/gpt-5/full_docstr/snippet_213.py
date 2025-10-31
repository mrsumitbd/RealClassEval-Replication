class LocalBedrockAgentCoreClient:
    '''Local Bedrock AgentCore client for invoking endpoints.'''

    def __init__(self, endpoint: str):
        '''Initialize the local client with the given endpoint.'''
        if not isinstance(endpoint, str) or not endpoint.strip():
            raise ValueError("endpoint must be a non-empty string")
        self.endpoint = endpoint.strip()

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        '''Invoke the endpoint with the given parameters.'''
        import json
        import urllib.request
        import urllib.error

        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id must be a non-empty string")
        if not isinstance(payload, str):
            raise ValueError("payload must be a string")
        if not isinstance(workload_access_token, str) or not workload_access_token.strip():
            raise ValueError(
                "workload_access_token must be a non-empty string")

        data = payload.encode("utf-8")

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "Authorization": f"Bearer {workload_access_token.strip()}",
            "x-session-id": session_id.strip(),
        }

        req = urllib.request.Request(
            url=self.endpoint,
            data=data,
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_body = resp.read().decode("utf-8", errors="replace")
                result = {
                    "status_code": resp.getcode(),
                    "headers": dict(resp.headers.items()),
                    "body": resp_body,
                }
                return result
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
            return {
                "status_code": e.code if hasattr(e, "code") else 500,
                "headers": dict(e.headers.items()) if hasattr(e, "headers") and e.headers else {},
                "body": body,
                "error": str(e),
            }
        except urllib.error.URLError as e:
            return {
                "status_code": 0,
                "headers": {},
                "body": "",
                "error": str(e),
            }
