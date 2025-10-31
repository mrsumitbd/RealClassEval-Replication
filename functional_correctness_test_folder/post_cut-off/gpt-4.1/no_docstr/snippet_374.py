
class ChannelIterator:

    def __init__(self, num_channels=0):
        self.num_channels = num_channels
        self.channels = self._generate_channels(num_channels)
        self._index = 0

    def _generate_channels(self, count):
        channels = []
        for i in range(count):
            h = i / count if count > 0 else 0
            s = 1.0
            v = 1.0
            rgb = self._hsv_to_rgb(h, s, v)
            channels.append(rgb)
        return channels

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        if s == 0.0:
            r = g = b = int(v * 255)
            return (r, g, b)
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        elif i == 5:
            r, g, b = v, p, q
        return (int(r * 255), int(g * 255), int(b * 255))

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= self.num_channels:
            raise StopIteration
        result = self.channels[self._index]
        self._index += 1
        return result

    def get_channel(self, index):
        if 0 <= index < self.num_channels:
            return self.channels[index]
        else:
            raise IndexError("Channel index out of range")

    def __len__(self):
        return self.num_channels
