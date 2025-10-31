class RawPacket:
    def __init__(self, packet):
        self.packet = packet

    def __getattr__(self, fieldname):
        # Try to get attribute from the underlying packet object
        if hasattr(self.packet, fieldname):
            return getattr(self.packet, fieldname)
        # If the packet is a mapping, try to fetch the key
        if isinstance(self.packet, dict) and fieldname in self.packet:
            return self.packet[fieldname]
        # If the packet is a sequence of bytes and the fieldname is an integer index
        if isinstance(self.packet, (bytes, bytearray)) and fieldname.isdigit():
            idx = int(fieldname)
            try:
                return self.packet[idx]
            except IndexError:
                pass
        raise AttributeError(
            f"'{type(self.packet).__name__}' object has no attribute '{fieldname}'")
