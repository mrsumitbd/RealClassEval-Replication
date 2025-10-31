
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class LambdaAsyncResponse:
    """
    Helper to invoke an AWS Lambda function asynchronously (or synchronously if requested).
    """

    def __init__(self, lambda_function_name=None, aws_region=None, capture_response=False, **kwargs):
        """
        Parameters
        ----------
        lambda_function_name : str, optional
            The name or ARN of the Lambda function to invoke.
        aws_region : str, optional
            AWS region where the Lambda function is deployed. If not provided, the default
            region configured in the environment or AWS SDK will be used.
        capture_response : bool, default False
            If True, the response payload from the Lambda invocation will be returned.
            If False, the invocation will be fire-and-forget (InvocationType='Event').
        **kwargs
            Additional keyword arguments passed to boto3.client() for Lambda.
        """
        if not lambda_function_name:
            raise ValueError("lambda_function_name must be provided")

        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region
        self.capture_response = capture_response

        # Create a Lambda client
        client_kwargs = {}
        if aws_region:
            client_kwargs['region_name'] = aws_region
        client_kwargs.update(kwargs)
        self.client = boto3.client('lambda', **client_kwargs)

    def send(self, task_path, args, kwargs):
        """
        Send a message to the Lambda function.

        Parameters
        ----------
        task_path : str
            Identifier for the task to be performed by the Lambda.
        args : list or tuple
            Positional arguments for the task.
        kwargs : dict
            Keyword arguments for the task.

        Returns
        -------
        str or None
            If capture_response is True, returns the decoded response payload.
            Otherwise, returns None.
        """
        message = {
            'task_path': task_path,
            'args': args,
            'kwargs': kwargs,
        }
        return self._send(message)

    def _send(self, message):
        """
        Internal method to invoke the Lambda function.

        Parameters
        ----------
        message : dict
            The payload to send to the Lambda function.

        Returns
        -------
        str or None
            If capture_response is True, returns the decoded response payload.
            Otherwise, returns None.
        """
        payload = json.dumps(message).encode('utf-8')
        invocation_type = 'RequestResponse' if self.capture_response else 'Event'

        try:
            response = self.client.invoke(
                FunctionName=self.lambda_function_name,
                InvocationType=invocation_type,
                Payload=payload,
            )
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError(
                f"Failed to invoke Lambda '{self.lambda_function_name}': {exc}") from exc

        if self.capture_response:
            # The payload is a streaming body; read and decode it.
            try:
                response_payload = response['Payload'].read()
                if isinstance(response_payload, bytes):
                    response_payload = response_payload.decode('utf-8')
                return response_payload
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to read Lambda response payload: {exc}") from exc

        return None
