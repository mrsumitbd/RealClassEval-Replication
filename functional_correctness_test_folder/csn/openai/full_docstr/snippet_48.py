
import datetime as dt
import struct
from datetime import timezone


class Datetime:
    '''Helps to pack and unpack datetime objects for the Broadlink protocol.'''

    @staticmethod
    def pack(datetime_obj: dt.datetime) -> bytes:
        '''Pack the timestamp to be sent over the Broadlink protocol.'''
        # Ensure the datetime is timezone-aware; assume UTC if naive
        if datetime_obj.tzinfo is None:
            datetime_obj = datetime_obj.replace(tzinfo=timezone.utc)
        # Convert to POSIX timestamp (seconds since epoch)
        ts = int(datetime_obj.timestamp())
        # Pack as 4-byte little-endian unsigned integer
        return struct.pack('<I', ts)

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        '''Unpack a timestamp received over the Broadlink protocol.'''
        # Expect at least 4 bytes; use the first 4
        if len(data) < 4:
            raise ValueError("Data too short to contain a timestamp")
        ts = struct.unpack('<I', data[:4])[0]
        # Convert back to datetime in UTC
        return dt.datetime.fromtimestamp(ts, tz=timezone.utc)

    @staticmethod
    def now() -> dt.datetime:
        '''Return the current date and time with timezone info.'''
        return dt.datetime.now(timezone.utc)
