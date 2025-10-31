class RawPacket:
    """RawPacket

    Wraps a packet such that:

        packet.raw.fieldname

    returns the value of fieldname as a raw value with no enumeration
    substitutions or DN to EU conversions applied.
    """
    __slots__ = ['_packet']

    def __init__(self, packet):
        """Creates a new RawPacket based on the given Packet."""
        self._packet = packet

    def __getattr__(self, fieldname):
        """Returns the value of the given packet fieldname as a raw
        value with no DN to EU conversion applied.
        """
        return self._packet._getattr(fieldname, raw=True)