
class PacketContext:

    def __init__(self, packet):
        '''Creates a new PacketContext for the given Packet.'''
        self.packet = packet
        self.context = {}

    def __getitem__(self, name):
        if name not in self.context:
            raise KeyError(f'Context item {name} not found')
        return self.context[name]

    # To make the class more useful, we can add methods to set and update context items.
    # However, as per the given skeleton, only __init__ and __getitem__ are implemented.

# Example usage:


class Packet:
    pass


packet = Packet()
context = PacketContext(packet)
try:
    print(context['test'])
except KeyError as e:
    print(e)

context.context['test'] = 'value'
print(context['test'])
