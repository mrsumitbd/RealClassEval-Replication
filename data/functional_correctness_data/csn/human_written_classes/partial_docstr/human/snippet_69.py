class S3RecordWriterFactory:
    """Factory for event protocol buffer files to S3."""

    def open(self, path):
        return S3RecordWriter(path)

    def directory_check(self, path):
        pass