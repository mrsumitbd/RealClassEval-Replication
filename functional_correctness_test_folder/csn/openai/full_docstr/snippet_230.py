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
        # 1. If the packet has a 'raw' attribute that is a mapping
        raw_attr = getattr(self._packet, 'raw', None)
        if isinstance(raw_attr, dict):
            if fieldname in raw_attr:
                return raw_attr[fieldname]

        # 2. If the packet provides a get_raw method
        get_raw = getattr(self._packet, 'get_raw', None)
        if callable(get_raw):
            return get_raw(fieldname)

        # 3. Try to access the attribute directly and see if it contains raw data
        attr = getattr(self._packet, fieldname, None)
        if attr is not None:
            # If the attribute itself has a 'raw' property
            if hasattr(attr, 'raw'):
                return attr.raw
            # If the attribute is a sequence, assume the first element is raw
            if isinstance(attr, (list, tuple)) and len(attr) > 0:
                return attr[0]

        # 4. If nothing found, raise AttributeError
        raise AttributeError(
            f"'{type(self._packet).__name__}' object has no raw field '{fieldname}'"
        )
