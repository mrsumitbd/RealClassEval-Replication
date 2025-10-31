
class ChannelIterator:

    def __init__(self, num_channels=0):
        self.num_channels = num_channels
        self.channels = self._generate_channels(num_channels)
        self.index = 0

    def _generate_channels(self, count):
        import random
        return [(random.random(), random.random(), random.random()) for _ in range(count)]

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        import colorsys
        return colorsys.hsv_to_rgb(h, s, v)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < self.num_channels:
            channel = self.channels[self.index]
            self.index += 1
            return channel
        else:
            raise StopIteration

    def get_channel(self, index):
        if 0 <= index < self.num_channels:
            return self.channels[index]
        else:
            raise IndexError("Index out of range")

    def __len__(self):
        return self.num_channels
