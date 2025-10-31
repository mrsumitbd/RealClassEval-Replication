from datetime import datetime, timedelta
import boto3

class BaseReader:

    def __init__(self, client_type, region_name=None, start_time=None, end_time=None, boto_client=None, raise_on_error=False):
        self.region_name = region_name
        if boto_client is not None:
            self.boto_client = boto_client
        else:
            kwargs = {'region_name': region_name} if region_name else {}
            self.boto_client = boto3.client(client_type, **kwargs)
        now = datetime.utcnow()
        self.start_time = start_time or now - timedelta(hours=1)
        self.end_time = end_time or now
        self.bytes_processed = 0
        self.iterator = self._reader()
        self.skipped_records = 0
        self.raise_on_error = raise_on_error

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iterator)