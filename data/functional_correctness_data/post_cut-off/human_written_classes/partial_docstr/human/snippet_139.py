class OutputDuplicator:
    """
    Output duplicator that writes to both a file and a stream.
    """

    def __init__(self, file_path, stream):
        self.file = open(file_path, 'a', encoding='utf-8')
        self.stream = stream

    def write(self, data):
        self.file.write(data)
        self.stream.write(data)
        self.file.flush()
        self.stream.flush()

    def flush(self):
        self.file.flush()
        self.stream.flush()

    def isatty(self):
        return self.stream.isatty()