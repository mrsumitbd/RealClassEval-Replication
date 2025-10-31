import sys

class Output:
    """A context manager to abstract out file or stdout"""

    def __init__(self, options):
        if options.output == '-':
            self.stream = sys.stdout
            self.output_file = None
        else:
            self.stream = open(options.output, 'w')
            self.output_file = self.stream

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, ecx_tb):
        if self.output_file is not None:
            self.output_file.close()
        return False