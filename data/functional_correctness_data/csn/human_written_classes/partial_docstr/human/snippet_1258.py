import datetime as dt
from posttroll.message import Message

class _PublisherHeartbeat:
    """Publisher for heartbeat."""

    def __init__(self, publisher):
        self.publisher = publisher
        self.subject = '/heartbeat/' + publisher.name
        self.lastbeat = dt.datetime(1900, 1, 1, tzinfo=dt.timezone.utc)

    def __call__(self, min_interval=0):
        if not min_interval or dt.datetime.now(dt.timezone.utc) - self.lastbeat >= dt.timedelta(seconds=min_interval):
            self.lastbeat = dt.datetime.now(dt.timezone.utc)
            LOGGER.debug('Publish heartbeat (min_interval is %.1f sec)', min_interval)
            self.publisher.send(Message(self.subject, 'beat', {'min_interval': min_interval}).encode())