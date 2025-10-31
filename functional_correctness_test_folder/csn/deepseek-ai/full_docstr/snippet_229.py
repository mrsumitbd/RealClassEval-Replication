
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
        self._packet = packet

    def __getitem__(self, name):
        '''Returns packet[name]'''
        return getattr(self._packet, name)
