
import boto3
import json


class LambdaAsyncResponse:
    '''
    Base Response Dispatcher class
    Can be used directly or subclassed if the method to send the message is changed.
    '''

    def __init__(self, lambda_function_name=None, aws_region=None, capture_response=False, **kwargs):
        ''' '''
        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region
        self.capture_response = capture_response
        self.kwargs = kwargs
        if self.lambda_function_name is not None and self.aws_region is not None:
            self.lambda_client = boto3.client(
                'lambda', region_name=self.aws_region)
        else:
            self.lambda_client = None

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
        if not self.lambda_client or not self.lambda_function_name:
            raise ValueError("Lambda client or function name not configured.")
        payload = json.dumps(message).encode('utf-8')
        invoke_args = {
            'FunctionName': self.lambda_function_name,
            'InvocationType': 'RequestResponse' if self.capture_response else 'Event',
            'Payload': payload
        }
        response = self.lambda_client.invoke(**invoke_args)
        if self.capture_response:
            response_payload = response.get('Payload')
            if response_payload:
                return json.loads(response_payload.read().decode('utf-8'))
            else:
                return None
        return None
