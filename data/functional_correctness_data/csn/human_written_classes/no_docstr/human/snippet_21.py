class IndentationContext:

    def __init__(self, increment=1):
        self.increment = increment

    def __enter__(self):
        _indentation_level.indent = getattr(_indentation_level, 'indent', 0) + self.increment

    def __exit__(self, exc_type, exc_val, exc_tb):
        _indentation_level.indent -= self.increment