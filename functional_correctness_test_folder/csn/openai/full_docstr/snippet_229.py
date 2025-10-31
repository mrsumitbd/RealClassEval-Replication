class PacketContext:
    '''PacketContext
    A PacketContext provides a simple wrapper around a Packet so that
    field accesses of the form:
        packet.fieldname
    may also be specified as:
        packet[fieldname]
    This latter syntax allows a PacketContext to be used as a symbol
    table when evaluating PacketExpressions.
    '''

    def __init__(self, packet):
        '''Creates a new PacketContext for the given Packet.'''
        self.packet = packet

    def __getitem__(self, name):
        '''Returns packet[name]'''
        # Try attribute access first
        try:
            return getattr(self.packet, name)
        except AttributeError:
            # Fallback to dict-like access if supported
            try:
                return self.packet[name]
            except Exception as exc:
                raise KeyError(name) from exc
