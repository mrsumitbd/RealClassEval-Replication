
import boto3
import json
import uuid


class LambdaAsyncResponse:

    def __init__(self, lambda_function_name=None, aws_region=None, capture_response=False, **kwargs):
        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region or 'us-east-1'
        self.capture_response = capture_response
        self.lambda_client = boto3.client(
            'lambda', region_name=self.aws_region)
        self.extra_kwargs = kwargs

    def send(self, task_path, args, kwargs):
        '''
        Create the message object and pass it to the actual sender.
        '''
        message = {
            'id': str(uuid.uuid4()),
            'task': task_path,
            'args': args,
            'kwargs': kwargs,
            'capture_response': self.capture_response
        }
        message.update(self.extra_kwargs)
        return self._send(message)

    def _send(self, message):
        '''
        Given a message, directly invoke the lamdba function for this task.
        '''
        payload = json.dumps(message).encode('utf-8')
        invocation_type = 'RequestResponse' if self.capture_response else 'Event'
        response = self.lambda_client.invoke(
            FunctionName=self.lambda_function_name,
            InvocationType=invocation_type,
            Payload=payload
        )
        if self.capture_response:
            resp_payload = response['Payload'].read()
            try:
                return json.loads(resp_payload)
            except Exception:
                return resp_payload
        else:
            return response
