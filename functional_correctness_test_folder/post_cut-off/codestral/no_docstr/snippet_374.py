
class ChannelIterator:

    def __init__(self, num_channels=0):
        self.num_channels = num_channels
        self.channels = self._generate_channels(num_channels)

    def _generate_channels(self, count):
        channels = []
        for i in range(count):
            h = i / count
            s = 1.0
            v = 1.0
            r, g, b = self._hsv_to_rgb(h, s, v)
            channels.append((r, g, b))
        return channels

    @staticmethod
    def _hsv_to_rgb(h, s, v):
        if s == 0.0:
            return v, v, v
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < self.num_channels:
            result = self.channels[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

    def get_channel(self, index):
        if 0 <= index < self.num_channels:
            return self.channels[index]
        else:
            raise IndexError("Channel index out of range")

    def __len__(self):
        return self.num_channels
