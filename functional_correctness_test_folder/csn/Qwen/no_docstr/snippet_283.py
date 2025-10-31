
class ProgressBarStream:

    def __init__(self, stream):
        self.stream = stream
        self.progress = 0

    def write(self, *args, **kwargs):
        self.stream.write(*args, **kwargs)
        self.update_progress(*args)

    def flush(self):
        self.stream.flush()

    def update_progress(self, *args):
        for arg in args:
            if isinstance(arg, str):
                self.progress += len(arg)
                self.show_progress()

    def show_progress(self):
        print(f"\rProgress: {self.progress} characters written",
              end='', file=self.stream)
