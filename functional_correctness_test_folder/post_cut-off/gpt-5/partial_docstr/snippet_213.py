class LocalBedrockAgentCoreClient:
    '''Local Bedrock AgentCore client for invoking endpoints.'''

    def __init__(self, endpoint: str):
        '''Initialize the local client with the given endpoint.'''
        from urllib.parse import urlparse

        if not isinstance(endpoint, str) or not endpoint.strip():
            raise ValueError("endpoint must be a non-empty string")
        parsed = urlparse(endpoint)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError("endpoint must be a valid http(s) URL")
        self._endpoint = endpoint
        self._timeout = 30  # seconds

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        import json
        import sys
        from urllib import request, error

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
            "Authorization": f"Bearer {workload_access_token}",
            "X-Session-Id": session_id,
        }

        req = request.Request(self._endpoint, data=data,
                              headers=headers, method="POST")

        try:
            with request.urlopen(req, timeout=self._timeout) as resp:
                resp_body_bytes = resp.read()
                resp_body = resp_body_bytes.decode(
                    resp.headers.get_content_charset() or "utf-8", errors="replace")
                content_type = resp.headers.get("Content-Type", "")
                result = {
                    "status_code": resp.getcode(),
                    "headers": dict(resp.headers.items()),
                    "body": resp_body,
                }
                if "application/json" in content_type.lower():
                    try:
                        result["json"] = json.loads(
                            resp_body) if resp_body else None
                    except json.JSONDecodeError:
                        # Keep raw body if JSON parsing fails
                        pass
                return result
        except error.HTTPError as e:
            body = None
            try:
                body_bytes = e.read()
                body = body_bytes.decode(getattr(e.headers, "get_content_charset", lambda: "utf-8")(
                ) or "utf-8", errors="replace") if body_bytes else None
            except Exception:
                body = None
            raise RuntimeError(
                f"HTTPError {e.code} while invoking endpoint: {body or e.reason}") from None
        except error.URLError as e:
            raise ConnectionError(
                f"Failed to connect to endpoint: {e.reason}") from None
        except Exception as e:
            raise RuntimeError(
                f"Unexpected error while invoking endpoint: {e}") from e
