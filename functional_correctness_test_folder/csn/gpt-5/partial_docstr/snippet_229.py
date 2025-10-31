class PacketContext:

    def __init__(self, packet):
        '''Creates a new PacketContext for the given Packet.'''
        self._packet = packet

    def __getitem__(self, name):
        if name in ('packet', '_packet', 'self', 'this'):
            return self._packet

        current = self._packet
        parts = name.split('.') if isinstance(name, str) else [name]

        for part in parts:
            if isinstance(current, dict):
                if part in current:
                    current = current[part]
                else:
                    raise KeyError(name)
            elif isinstance(current, (list, tuple)) and isinstance(part, str) and part.isdigit():
                idx = int(part)
                try:
                    current = current[idx]
                except (IndexError, TypeError):
                    raise KeyError(name)
            else:
                if hasattr(current, part):
                    current = getattr(current, part)
                else:
                    raise KeyError(name)

        return current
