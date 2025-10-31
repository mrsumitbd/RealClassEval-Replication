
import json
import boto3


class LambdaAsyncResponse:

    def __init__(self, lambda_function_name=None, aws_region=None, capture_response=False, **kwargs):
        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region
        self.capture_response = capture_response
        self.lambda_client = boto3.client(
            'lambda', region_name=aws_region) if aws_region else boto3.client('lambda')

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
        Given a message, directly invoke the lamdba function for this task.
        '''
        response = self.lambda_client.invoke(
            FunctionName=self.lambda_function_name,
            InvocationType='Event' if not self.capture_response else 'RequestResponse',
            Payload=json.dumps(message)
        )
        return response
