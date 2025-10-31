import json
from typing import Any, Dict, Optional

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except Exception:  # pragma: no cover
    boto3 = None
    BotoCoreError = Exception
    ClientError = Exception


class LambdaAsyncResponse:

    def __init__(self, lambda_function_name: Optional[str] = None, aws_region: Optional[str] = None, capture_response: bool = False, **kwargs):
        if not lambda_function_name:
            raise ValueError("lambda_function_name is required")
        if boto3 is None:
            raise RuntimeError("boto3 is required to use LambdaAsyncResponse")
        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region
        self.capture_response = capture_response
        self._invoke_extra: Dict[str, Any] = {}
        # Allow passing additional invoke parameters, e.g., Qualifier, ClientContext
        if kwargs:
            self._invoke_extra.update(kwargs)
        self._client = boto3.client("lambda", region_name=self.aws_region)

    def send(self, task_path, args, kwargs):
        message = {
            "task": task_path,
            "args": args if args is not None else [],
            "kwargs": kwargs if kwargs is not None else {},
        }
        return self._send(message)

    def _send(self, message):
        try:
            payload_bytes = json.dumps(
                message, default=self._json_default).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise TypeError(
                f"Message is not JSON serializable: {exc}") from exc

        params: Dict[str, Any] = {
            "FunctionName": self.lambda_function_name,
            "InvocationType": "RequestResponse" if self.capture_response else "Event",
            "Payload": payload_bytes,
        }
        # Merge any extra invoke parameters provided at init
        if self._invoke_extra:
            params.update(self._invoke_extra)

        try:
            response = self._client.invoke(**params)
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(
                f"Failed to invoke Lambda '{self.lambda_function_name}': {exc}") from exc

        status_code = response.get("StatusCode")
        request_id = response.get("ResponseMetadata", {}).get("RequestId")

        if not self.capture_response:
            return {
                "StatusCode": status_code,
                "RequestId": request_id,
            }

        # When capturing response, parse Payload
        payload_stream = response.get("Payload")
        raw = None
        parsed = None
        if payload_stream is not None:
            try:
                raw = payload_stream.read()
            finally:
                try:
                    payload_stream.close()
                except Exception:
                    pass
            if isinstance(raw, (bytes, bytearray)):
                text = raw.decode("utf-8") if raw else ""
            else:
                text = str(raw) if raw is not None else ""
            # Try to parse JSON; fall back to raw text
            try:
                parsed = json.loads(text) if text else None
            except json.JSONDecodeError:
                parsed = text

        result = {
            "StatusCode": status_code,
            "RequestId": request_id,
            "FunctionError": response.get("FunctionError"),
            "ExecutedVersion": response.get("ExecutedVersion"),
            "Payload": parsed,
        }
        return result

    @staticmethod
    def _json_default(obj):
        raise TypeError(
            f"Object of type {type(obj).__name__} is not JSON serializable")
