
import boto3
import json


class LambdaAsyncResponse:

    def __init__(self, lambda_function_name=None, aws_region=None, capture_response=False, **kwargs):
        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region
        self.capture_response = capture_response
        self.client = boto3.client('lambda', region_name=self.aws_region)
        self.kwargs = kwargs

    def send(self, task_path, args, kwargs):
        payload = {
            'task_path': task_path,
            'args': args,
            'kwargs': kwargs
        }
        self._send(payload)

    def _send(self, message):
        response = self.client.invoke(
            FunctionName=self.lambda_function_name,
            InvocationType='Event' if not self.capture_response else 'RequestResponse',
            Payload=json.dumps(message),
            **self.kwargs
        )
        if self.capture_response:
            return response['Payload'].read().decode('utf-8')
