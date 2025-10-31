class LocalBedrockAgentCoreClient:
    def __init__(self, endpoint: str):
        if not isinstance(endpoint, str) or not endpoint.strip():
            raise ValueError("endpoint must be a non-empty string.")
        self._endpoint = endpoint.strip().rstrip("/")

    def invoke_endpoint(self, session_id: str, payload: str, workload_access_token: str):
        import json
        from urllib import request, error

        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id must be a non-empty string.")
        if not isinstance(payload, str):
            raise ValueError("payload must be a string.")
        if not isinstance(workload_access_token, str) or not workload_access_token.strip():
            raise ValueError(
                "workload_access_token must be a non-empty string.")

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain;q=0.9, */*;q=0.8",
            "Authorization": f"Bearer {workload_access_token}",
            "X-Session-Id": session_id,
        }

        body = {
            "sessionId": session_id,
            "payload": None,
        }

        try:
            # Try to preserve JSON if payload is JSON, otherwise send as a raw string
            body["payload"] = json.loads(payload)
        except json.JSONDecodeError:
            body["payload"] = payload

        data_bytes = json.dumps(body).encode("utf-8")
        req = request.Request(self._endpoint, data=data_bytes,
                              headers=headers, method="POST")

        try:
            with request.urlopen(req, timeout=30) as resp:
                resp_body = resp.read()
                resp_text = resp_body.decode("utf-8", errors="replace")
                try:
                    parsed = json.loads(resp_text)
                except json.JSONDecodeError:
                    parsed = resp_text
                return {
                    "status_code": getattr(resp, "status", getattr(resp, "code", 200)),
                    "headers": dict(resp.headers.items()),
                    "body": parsed,
                }
        except error.HTTPError as e:
            resp_text = e.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(resp_text)
            except json.JSONDecodeError:
                parsed = resp_text
            return {
                "status_code": e.code,
                "headers": dict(e.headers.items()) if e.headers else {},
                "body": parsed,
            }
        except error.URLError as e:
            raise ConnectionError(
                f"Failed to reach endpoint {self._endpoint}: {e}") from e
