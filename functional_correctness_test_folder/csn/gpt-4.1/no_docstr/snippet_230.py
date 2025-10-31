
class RawPacket:

    def __init__(self, packet):
        self._packet = packet

    def __getattr__(self, fieldname):
        try:
            return self._packet[fieldname]
        except KeyError:
            raise AttributeError(
                f"'RawPacket' object has no attribute '{fieldname}'")
