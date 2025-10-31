
import colorsys


class ChannelIterator:

    def __init__(self, num_channels=0):
        self.num_channels = num_channels
        self.current = 0
        self.channels = self._generate_channels(num_channels)

    def _generate_channels(self, count):
        channels = []
        for i in range(count):
            hue = i / max(1, count)
            rgb = self._hsv_to_rgb(hue, 1.0, 1.0)
            channels.append(rgb)
        return channels

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        return colorsys.hsv_to_rgb(h, s, v)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < len(self.channels):
            channel = self.channels[self.current]
            self.current += 1
            return channel
        else:
            raise StopIteration

    def get_channel(self, index):
        if 0 <= index < len(self.channels):
            return self.channels[index]
        raise IndexError("Index out of range")

    def __len__(self):
        return len(self.channels)
