
class RawPacket:
    '''RawPacket
    Wraps a packet such that:
        packet.raw.fieldname
    returns the value of fieldname as a raw value with no enumeration
    substitutions or DN to EU conversions applied.
    '''

    def __init__(self, packet):
        '''Creates a new RawPacket based on the given Packet.'''
        self._packet = packet

    def __getattr__(self, fieldname):
        '''Returns the value of the given packet fieldname as a raw
        value with no DN to EU conversion applied.
        '''
        # Try to access the raw value of the field from the underlying packet
        # If the packet has a 'raw' attribute, use it; else, get the field directly
        if hasattr(self._packet, 'get_raw'):
            return self._packet.get_raw(fieldname)
        elif hasattr(self._packet, 'raw') and hasattr(self._packet.raw, fieldname):
            return getattr(self._packet.raw, fieldname)
        elif hasattr(self._packet, fieldname):
            return getattr(self._packet, fieldname)
        else:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{fieldname}'")
