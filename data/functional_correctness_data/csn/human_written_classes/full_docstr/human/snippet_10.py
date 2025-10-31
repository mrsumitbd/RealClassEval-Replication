import json
import uuid

class LambdaAsyncResponse:
    """
    Base Response Dispatcher class
    Can be used directly or subclassed if the method to send the message is changed.
    """

    def __init__(self, lambda_function_name=None, aws_region=None, capture_response=False, **kwargs):
        """ """
        if kwargs.get('boto_session'):
            self.client = kwargs.get('boto_session').client('lambda')
        else:
            self.client = LAMBDA_CLIENT
        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region
        if capture_response:
            if ASYNC_RESPONSE_TABLE is None:
                print("Warning! Attempted to capture a response without async_response_table configured in settings (you won't capture async responses).")
                capture_response = False
                self.response_id = 'MISCONFIGURED'
            else:
                self.response_id = str(uuid.uuid4())
        else:
            self.response_id = None
        self.capture_response = capture_response

    def send(self, task_path, args, kwargs):
        """
        Create the message object and pass it to the actual sender.
        """
        message = {'task_path': task_path, 'capture_response': self.capture_response, 'response_id': self.response_id, 'args': args, 'kwargs': kwargs}
        self._send(message)
        return self

    def _send(self, message):
        """
        Given a message, directly invoke the lamdba function for this task.
        """
        message['command'] = 'zappa.asynchronous.route_lambda_task'
        payload = json.dumps(message).encode('utf-8')
        if len(payload) > LAMBDA_ASYNC_PAYLOAD_LIMIT:
            raise AsyncException('Payload too large for async Lambda call')
        self.response = self.client.invoke(FunctionName=self.lambda_function_name, InvocationType='Event', Payload=payload)
        self.sent = self.response.get('StatusCode', 0) == 202