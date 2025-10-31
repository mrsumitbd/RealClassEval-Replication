
import boto3
import json


class LambdaAsyncResponse:

    def __init__(self, lambda_function_name=None, aws_region=None, capture_response=False, **kwargs):

        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region
        self.capture_response = capture_response
        self.kwargs = kwargs
        self.lambda_client = boto3.client('lambda', region_name=aws_region)

    def send(self, task_path, args, kwargs):

        message = {
            'task_path': task_path,
            'args': args,
            'kwargs': kwargs,
            'capture_response': self.capture_response
        }
        return self._send(message)

    def _send(self, message):

        response = self.lambda_client.invoke(
            FunctionName=self.lambda_function_name,
            InvocationType='Event' if not self.capture_response else 'RequestResponse',
            Payload=json.dumps(message)
        )
        if self.capture_response:
            return json.loads(response['Payload'].read().decode('utf-8'))
        return response
