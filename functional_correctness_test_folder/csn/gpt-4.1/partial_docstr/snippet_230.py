
class RawPacket:

    def __init__(self, packet):
        self._packet = packet

    def __getattr__(self, fieldname):
        '''Returns the value of the given packet fieldname as a raw
        value with no DN to EU conversion applied.
        '''
        try:
            return self._packet[fieldname]
        except KeyError:
            raise AttributeError(
                f"'RawPacket' object has no attribute '{fieldname}'")
