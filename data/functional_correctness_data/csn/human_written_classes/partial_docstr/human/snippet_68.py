class GCSRecordWriterFactory:
    """Factory for event protocol buffer files to Google Cloud Storage."""

    def open(self, path):
        return GCSRecordWriter(path)

    def directory_check(self, path):
        pass