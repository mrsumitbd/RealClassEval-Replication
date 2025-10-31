class TaskCaptureOutput:

    def __init__(self, code):
        self.code = code

    def __call__(self, shell):
        return run_code(shell.run_code, self.code)