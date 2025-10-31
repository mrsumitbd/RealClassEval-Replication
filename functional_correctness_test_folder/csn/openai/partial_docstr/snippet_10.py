
import json
import logging
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

log = logging.getLogger(__name__)


class LambdaAsyncResponse:
    """
    Helper to send asynchronous tasks to an AWS Lambda function.

    Parameters
    ----------
    lambda_function_name : str, optional
        Name or ARN of the Lambda function to invoke.
    aws_region : str, optional
        AWS region where the Lambda function resides.
    capture_response : bool, default False
        If True, the response payload from the Lambda invocation is returned.
    **kwargs
        Additional keyword arguments are stored for future use.
    """

    def __init__(
        self,
        lambda_function_name: Optional[str] = None,
        aws_region: Optional[str] = None,
        capture_response: bool = False,
        **kwargs: Any,
    ):
        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region
        self.capture_response = capture_response
        self._extra_kwargs = kwargs
        self._lambda_client = None

        if not self.lambda_function_name:
            raise ValueError("lambda_function_name must be provided")
        if not self.aws_region:
            raise ValueError("aws_region must be provided")

    def _get_client(self):
        """Return a cached boto3 Lambda client."""
        if self._lambda_client is None:
            self._lambda_client = boto3.client(
                "lambda", region_name=self.aws_region)
        return self._lambda_client

    def send(self, task_path: str, args: Any, kwargs: Dict[str, Any]):
        """
        Create the message object and pass it to the actual sender.

        Parameters
        ----------
        task_path : str
            The dotted path to the task function.
        args : Any
            Positional arguments for the task.
        kwargs : dict
            Keyword arguments for the task.

        Returns
        -------
        Any
            The response payload if capture_response is True, otherwise None.
        """
        message = {
            "task_path": task_path,
            "args": args,
            "kwargs": kwargs,
        }
        return self._send(message)

    def _send(self, message: Dict[str, Any]):
        """
        Given a message, directly invoke the Lambda function for this task.

        Parameters
        ----------
        message : dict
            The payload to send to Lambda.

        Returns
        -------
        Any
            The response payload if capture_response is True, otherwise None.
        """
        client = self._get_client()
        invocation_type = "Event" if not self.capture_response else "RequestResponse"

        try:
            response = client.invoke(
                FunctionName=self.lambda_function_name,
                InvocationType=invocation_type,
                Payload=json.dumps(message).encode("utf-8"),
                **self._extra_kwargs,
            )
        except (BotoCoreError, ClientError) as exc:
            log.exception("Failed to invoke Lambda function %s",
                          self.lambda_function_name)
            raise RuntimeError(f"Lambda invocation failed: {exc}") from exc

        if self.capture_response:
            payload_bytes = response.get("Payload", b"")
            try:
                payload_str = payload_bytes.read().decode("utf-8")
                return json.loads(payload_str)
            except Exception as exc:
                log.exception("Failed to decode Lambda response payload")
                raise RuntimeError(
                    f"Failed to decode Lambda response: {exc}") from exc

        return None
