
import boto3
import json


class LambdaAsyncResponse:

    def __init__(self, lambda_function_name=None, aws_region=None, capture_response=False, **kwargs):
        self.lambda_function_name = lambda_function_name
        self.aws_region = aws_region
        self.capture_response = capture_response
        self.kwargs = kwargs
        self.client = boto3.client(
            'lambda', region_name=self.aws_region, **self.kwargs)

    def send(self, task_path, args, kwargs):
        message = {
            'task_path': task_path,
            'args': args,
            'kwargs': kwargs
        }
        return self._send(message)

    def _send(self, message):
        payload = json.dumps(message).encode('utf-8')
        invocation_type = 'RequestResponse' if self.capture_response else 'Event'
        response = self.client.invoke(
            FunctionName=self.lambda_function_name,
            InvocationType=invocation_type,
            Payload=payload
        )
        if self.capture_response:
            response_payload = response['Payload'].read()
            try:
                return json.loads(response_payload)
            except Exception:
                return response_payload
        else:
            return response
