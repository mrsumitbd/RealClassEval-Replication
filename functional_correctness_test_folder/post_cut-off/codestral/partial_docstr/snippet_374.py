
import colorsys
import random


class ChannelIterator:

    def __init__(self, num_channels=0):
        self.channels = []
        self._generate_channels(num_channels)

    def _generate_channels(self, count):
        for _ in range(count):
            h = random.random()
            s = 0.7 + random.random() * 0.3
            v = 0.7 + random.random() * 0.3
            r, g, b = self._hsv_to_rgb(h, s, v)
            self.channels.append(
                {'label': f'Channel {len(self.channels) + 1}', 'color': (r, g, b)})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(r * 255), int(g * 255), int(b * 255)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.channels) == 0:
            self._generate_channels(1)
        return self.channels.pop(0)

    def get_channel(self, index):
        if index < len(self.channels):
            return self.channels[index]
        else:
            self._generate_channels(index - len(self.channels) + 1)
            return self.channels[index]

    def __len__(self):
        return len(self.channels)
