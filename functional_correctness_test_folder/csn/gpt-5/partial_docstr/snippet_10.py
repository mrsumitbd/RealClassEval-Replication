class LambdaAsyncResponse:

    def __init__(self, lambda_function_name=None, aws_region=None, capture_response=False, **kwargs):
        self.lambda_function_name = lambda_function_name
        self.capture_response = bool(capture_response)

        self._client = kwargs.pop("lambda_client", None)
        self._client_kwargs = kwargs

        if self._client is None:
            try:
                import boto3
            except ImportError as e:
                raise RuntimeError(
                    "boto3 is required to use LambdaAsyncResponse without providing a lambda_client") from e
            client_kwargs = dict(self._client_kwargs)
            if aws_region:
                client_kwargs.setdefault("region_name", aws_region)
            self._client = boto3.client("lambda", **client_kwargs)

        if not self.lambda_function_name:
            raise ValueError("lambda_function_name must be provided")

    def send(self, task_path, args, kwargs):
        '''
        Create the message object and pass it to the actual sender.
        '''
        if not isinstance(task_path, str) or not task_path:
            raise ValueError("task_path must be a non-empty string")
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}

        if not isinstance(args, (list, tuple)):
            raise TypeError("args must be a list or tuple")
        if not isinstance(kwargs, dict):
            raise TypeError("kwargs must be a dict")

        message = {
            "task_path": task_path,
            "args": list(args),
            "kwargs": dict(kwargs),
        }
        return self._send(message)

    def _send(self, message):
        '''
        Given a message, directly invoke the lamdba function for this task.
        '''
        try:
            import json
        except ImportError as e:
            raise RuntimeError("json module is required") from e

        invocation_type = "RequestResponse" if self.capture_response else "Event"
        payload_bytes = json.dumps(
            message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

        response = self._client.invoke(
            FunctionName=self.lambda_function_name,
            InvocationType=invocation_type,
            Payload=payload_bytes,
        )

        result = {
            "status_code": response.get("StatusCode"),
            "request_id": (response.get("ResponseMetadata") or {}).get("RequestId"),
            "function_error": response.get("FunctionError"),
            "log_result": response.get("LogResult"),
            "payload": None,
        }

        payload_stream = response.get("Payload")
        if payload_stream is not None:
            try:
                raw = payload_stream.read()
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8", errors="replace")
                try:
                    parsed = json.loads(raw) if raw else None
                    result["payload"] = parsed
                except Exception:
                    result["payload"] = raw
            finally:
                try:
                    payload_stream.close()
                except Exception:
                    pass

        return result
