import json

class JsonWriter:
    """Utility for dumping rows as JSON objects."""

    def __init__(self, out):
        """Initialize with output destination."""
        self._out = out

    def writerow(self, row):
        """Write a single row."""
        json_text = json.dumps(row)
        if isinstance(json_text, bytes):
            json_text = json_text.decode('utf-8')
        self._out.write(json_text)
        self._out.write(u'\n')