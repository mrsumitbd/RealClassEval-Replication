class CaptureErrors:

    def __init__(self, output):
        self.output = output

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exception, traceback):
        if exc_type is not None:
            self.output.append({'type': 'backend-error', 'payload': str(exception)})
            return True