
import datetime as dt
import struct
import time


class Datetime:
    '''Helps to pack and unpack datetime objects for the Broadlink protocol.'''
    @staticmethod
    def pack(datetime: dt.datetime) -> bytes:
        '''Pack the timestamp to be sent over the Broadlink protocol.'''
        timestamp = int(datetime.timestamp())
        return struct.pack('<I', timestamp)

    @staticmethod
    def unpack(data: bytes) -> dt.datetime:
        '''Unpack a timestamp received over the Broadlink protocol.'''
        timestamp = struct.unpack('<I', data)[0]
        return dt.datetime.fromtimestamp(timestamp)

    @staticmethod
    def now() -> dt.datetime:
        '''Return the current date and time with timezone info.'''
        return dt.datetime.now(dt.timezone.utc)
