import os
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
    '''
    Base Response Dispatcher class
    Can be used directly or subclassed if the method to send the message is changed.
    '''

    def __init__(self, lambda_function_name: Optional[str] = None, aws_region: Optional[str] = None, capture_response: bool = False, **kwargs):
        '''
        Initialize the dispatcher with Lambda function details.

        - lambda_function_name: Name or ARN of the target Lambda function.
        - aws_region: AWS region to use. Falls back to AWS_REGION or AWS_DEFAULT_REGION env vars.
        - capture_response: If True, waits for and returns the Lambda response payload. Otherwise invokes asynchronously.
        - kwargs: Additional boto3.client('lambda', ...) keyword args.
        '''
        self.lambda_function_name = lambda_function_name or os.getenv(
            "LAMBDA_FUNCTION_NAME")
        if not self.lambda_function_name:
            raise ValueError(
                "Lambda function name must be provided via parameter or LAMBDA_FUNCTION_NAME environment variable.")

        self.aws_region = aws_region or os.getenv(
            "AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
        if not self.aws_region:
            raise ValueError(
                "AWS region must be provided via parameter or AWS_REGION/AWS_DEFAULT_REGION environment variable.")

        self.capture_response = bool(capture_response)

        if boto3 is None:
            raise RuntimeError(
                "boto3 is required to use LambdaAsyncResponse but is not installed.")

        # Allow passing through additional boto3 client args via kwargs (e.g., endpoint_url, config, credentials)
        self._client = boto3.client(
            "lambda", region_name=self.aws_region, **kwargs)

    def send(self, task_path: str, args: Any, kwargs: Dict[str, Any]):
        '''
        Create the message object and pass it to the actual sender.
        '''
        message = {
            "task_path": task_path,
            "args": args,
            "kwargs": kwargs or {},
        }
        return self._send(message)

    def _send(self, message: Dict[str, Any]):
        '''
        Given a message, directly invoke the lamdba function for this task.
        '''
        try:
            payload_bytes = json.dumps(message, default=str).encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Failed to serialize message to JSON: {exc}") from exc

        invocation_type = "RequestResponse" if self.capture_response else "Event"

        try:
            response = self._client.invoke(
                FunctionName=self.lambda_function_name,
                InvocationType=invocation_type,
                Payload=payload_bytes,
            )
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(
                f"Error invoking Lambda function '{self.lambda_function_name}': {exc}") from exc

        if self.capture_response:
            # Return parsed JSON payload if possible; otherwise return raw string.
            payload_stream = response.get("Payload")
            if payload_stream is None:
                return None
            raw = payload_stream.read()
            if not raw:
                return None
            try:
                return json.loads(raw.decode("utf-8"))
            except Exception:
                try:
                    return raw.decode("utf-8")
                except Exception:
                    return raw

        # For async invocation, return minimal metadata
        return {
            "StatusCode": response.get("StatusCode"),
            "RequestId": response.get("ResponseMetadata", {}).get("RequestId"),
        }
