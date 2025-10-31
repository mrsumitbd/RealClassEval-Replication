class RawPacket:

    def __init__(self, packet):
        self._packet = packet

    def __getattr__(self, fieldname):
        """Returns the value of the given packet fieldname as a raw
        value with no DN to EU conversion applied.
        """
        pkt = self._packet
        # Try dictionary lookup first
        if isinstance(pkt, dict):
            if fieldname in pkt:
                return pkt[fieldname]
        # Try attribute lookup
        if hasattr(pkt, fieldname):
            return getattr(pkt, fieldname)
        # If not found, raise AttributeError
        raise AttributeError(
            f"'{type(pkt).__name__}' object has no attribute '{fieldname}'")
