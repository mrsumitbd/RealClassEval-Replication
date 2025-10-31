
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class LambdaAsyncResponse:
    '''
    Base Response Dispatcher class
    Can be used directly or subclassed if the method to send the message is changed.
    '''

    def __init__(self, lambda_function_name=None, aws_region=None, capture_response=False, **kwargs):
        '''Initialize the dispatcher with the target Lambda function and AWS region.'''
        if not lambda_function_name:
            raise ValueError("lambda_function_name must be provided")
        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region
        self.capture_response = capture_response
        # Create a Lambda client; allow additional client kwargs
        self.client = boto3.client(
            'lambda', region_name=self.aws_region, **kwargs)

    def send(self, task_path, args, kwargs):
        '''
        Create the message object and pass it to the actual sender.
        '''
        message = {
            'task_path': task_path,
            'args': args,
            'kwargs': kwargs
        }
        return self._send(message)

    def _send(self, message):
        '''
        Given a message, directly invoke the lambda function for this task.
        '''
        payload = json.dumps(message).encode('utf-8')
        invocation_type = 'RequestResponse' if self.capture_response else 'Event'
        try:
            response = self.client.invoke(
                FunctionName=self.lambda_function_name,
                InvocationType=invocation_type,
                Payload=payload
            )
        except (BotoCoreError, ClientError) as exc:
            # Log or re-raise as needed; here we simply re-raise
            raise RuntimeError(
                f"Failed to invoke Lambda '{self.lambda_function_name}': {exc}") from exc

        if self.capture_response:
            # Read the response payload
            try:
                response_payload = response.get('Payload')
                if response_payload is not None:
                    # response_payload is a StreamingBody; read it
                    body_bytes = response_payload.read()
                    body_str = body_bytes.decode('utf-8')
                    return json.loads(body_str)
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to parse Lambda response: {exc}") from exc
        return None
