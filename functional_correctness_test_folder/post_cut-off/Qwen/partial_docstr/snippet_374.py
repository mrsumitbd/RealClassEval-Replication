
import random


class ChannelIterator:

    def __init__(self, num_channels=0):
        self.channels = []
        self._generate_channels(num_channels)

    def _generate_channels(self, count):
        for _ in range(count):
            h = random.uniform(0, 1)
            s = random.uniform(0.5, 1)
            v = random.uniform(0.5, 1)
            rgb = self._hsv_to_rgb(h, s, v)
            label = f"Channel_{len(self.channels)}"
            self.channels.append({'label': label, 'color': rgb})

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        r, g, b = 0, 0, 0
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)

        if i % 6 == 0:
            r, g, b = v, t, p
        elif i % 6 == 1:
            r, g, b = q, v, p
        elif i % 6 == 2:
            r, g, b = p, v, t
        elif i % 6 == 3:
            r, g, b = p, q, v
        elif i % 6 == 4:
            r, g, b = t, p, v
        elif i % 6 == 5:
            r, g, b = v, p, q

        return int(r * 255), int(g * 255), int(b * 255)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self.channels):
            result = self.channels[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

    def get_channel(self, index):
        if 0 <= index < len(self.channels):
            return self.channels[index]
        else:
            raise IndexError("Index out of range")

    def __len__(self):
        return len(self.channels)
