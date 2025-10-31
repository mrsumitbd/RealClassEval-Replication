
import boto3
import json


class LambdaAsyncResponse:
    '''
    Base Response Dispatcher class
    Can be used directly or subclassed if the method to send the message is changed.
    '''

    def __init__(self, lambda_function_name=None, aws_region=None, capture_response=False, **kwargs):
        '''
        Initialize the LambdaAsyncResponse with the given parameters.

        :param lambda_function_name: The name of the Lambda function to invoke.
        :param aws_region: The AWS region where the Lambda function is located.
        :param capture_response: Whether to capture the response from the Lambda function.
        :param kwargs: Additional keyword arguments.
        '''
        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region
        self.capture_response = capture_response
        self.kwargs = kwargs
        self.lambda_client = boto3.client('lambda', region_name=aws_region)

    def send(self, task_path, args, kwargs):
        '''
        Create the message object and pass it to the actual sender.

        :param task_path: The path of the task to be executed.
        :param args: Positional arguments for the task.
        :param kwargs: Keyword arguments for the task.
        '''
        message = {
            'task_path': task_path,
            'args': args,
            'kwargs': kwargs
        }
        self._send(message)

    def _send(self, message):
        '''
        Given a message, directly invoke the Lambda function for this task.

        :param message: The message to be sent to the Lambda function.
        '''
        response = self.lambda_client.invoke(
            FunctionName=self.lambda_function_name,
            InvocationType='Event' if not self.capture_response else 'RequestResponse',
            Payload=json.dumps(message)
        )
        if self.capture_response:
            return response
