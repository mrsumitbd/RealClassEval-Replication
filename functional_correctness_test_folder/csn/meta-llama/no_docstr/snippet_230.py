
class RawPacket:

    def __init__(self, packet):
        self.__dict__['_packet'] = packet

    def __getattr__(self, fieldname):
        return self._packet.get(fieldname)
